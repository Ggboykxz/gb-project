#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

struct AppState {
    backend_running: AtomicBool,
}

#[tauri::command]
fn get_backend_status(state: tauri::State<AppState>) -> bool {
    state.backend_running.load(Ordering::Relaxed)
}

#[tokio::main]
async fn main() {
    // Start Python FastAPI sidecar
    let backend_running = Arc::new(AtomicBool::new(false));
    
    #[cfg(not(target_os = "linux"))]
    let backend_cmd = Command::new("python")
        .arg("../backend/main.py")
        .current_dir("..")
        .spawn();

    #[cfg(target_os = "linux")]
    let backend_cmd = Command::new("python3")
        .arg("../backend/main.py")
        .current_dir("..")
        .spawn();

    match backend_cmd {
        Ok(_) => {
            println!("Backend FastAPI started");
            backend_running.store(true, Ordering::Relaxed);
            
            // Wait for backend to be ready
            sleep(Duration::from_secs(2)).await;
        }
        Err(e) => {
            eprintln!("Failed to start backend: {}", e);
        }
    }

    let state = AppState {
        backend_running: AtomicBool::new(backend_running.load(Ordering::Relaxed)),
    };

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(state)
        .invoke_handler(tauri::generate_handler![get_backend_status])
        .run(tauri::generate_context!())
        .expect("error while running GabonEdu Campus");
}
