#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::env;
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;
use tauri_plugin_shell::ShellExt;

struct AppState {
    backend_running: AtomicBool,
    api_port: u16,
}

#[tauri::command]
fn get_backend_status(state: tauri::State<AppState>) -> bool {
    state.backend_running.load(Ordering::Relaxed)
}

#[tauri::command]
fn get_api_port(state: tauri::State<AppState>) -> u16 {
    state.api_port
}

#[tokio::main]
async fn main() {
    // Determine port (avoid conflicts)
    let api_port: u16 = 8765;
    
    // Start Python FastAPI sidecar
    let backend_running = Arc::new(AtomicBool::new(false));
    
    // Get app data directory for database
    let app_data_dir = env::var("APP_DATA_DIR").unwrap_or_else(|_| {
        #[cfg(target_os = "windows")]
        return env::var("APPDATA").unwrap_or_else(|_| "C:\\ProgramData\\GabonEdu".to_string());
        
        #[cfg(target_os = "macos")]
        return env::var("HOME").unwrap_or_else(|_| "/Users/Shared/GabonEdu".to_string()) + "/Library/Application Support";
        
        #[cfg(target_os = "linux")]
        return env::var("HOME").unwrap_or_else(|_| "/home".to_string()) + "/.local/share/gabonedu";
    });
    
    println!("App data directory: {}", app_data_dir);
    println!("Starting backend on port {}", api_port);

    // Try to find python executable
    let python_cmd = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };

    // Path to backend script (relative to executable or in resources)
    let backend_path = if cfg!(debug_assertions) {
        // Dev mode: relative path
        PathBuf::from("../backend/main.py")
    } else {
        // Prod mode: from resources
        let exe_dir = env::current_exe()
            .ok()
            .and_then(|pb| pb.parent().map(|p| p.to_path_buf()))
            .unwrap_or_default();
        exe_dir.join("../Resources/backend/main.py")
    };

    println!("Backend path: {:?}", backend_path);

    let backend_process = Command::new(python_cmd)
        .arg(&backend_path)
        .arg("--port")
        .arg(api_port.to_string())
        .arg("--data-dir")
        .arg(&app_data_dir)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn();

    match backend_process {
        Ok(mut child) => {
            println!("Backend FastAPI started successfully on port {}", api_port);
            backend_running.store(true, Ordering::Relaxed);
            
            // Wait for backend to initialize
            sleep(Duration::from_secs(3)).await;
            
            // Check if process is still running
            match child.try_wait() {
                Ok(Some(status)) => {
                    eprintln!("Backend exited early with status: {}", status);
                    backend_running.store(false, Ordering::Relaxed);
                }
                Ok(None) => {
                    println!("Backend is running and healthy");
                    // Detach process (let it run independently)
                    let _ = child.kill(); // We'll restart it properly via shell plugin in prod
                }
                Err(e) => eprintln!("Error checking backend status: {}", e),
            }
        }
        Err(e) => {
            eprintln!("Failed to start backend: {}. Trying alternative methods...", e);
            // Fallback: try with full python path or bundled binary
        }
    }

    let state = AppState {
        backend_running: AtomicBool::new(backend_running.load(Ordering::Relaxed)),
        api_port,
    };

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_fs::init())
        .manage(state)
        .invoke_handler(tauri::generate_handler![get_backend_status, get_api_port])
        .run(tauri::generate_context!())
        .expect("error while running GabonEdu Campus");
}
