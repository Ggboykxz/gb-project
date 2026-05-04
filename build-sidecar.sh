#!/usr/bin/env bash
# Script de build du sidecar Python pour GabonEdu Campus
# Génère un exécutable unique avec PyInstaller

set -e

echo "🔨 Build du sidecar Python FastAPI..."

# Vérifier les dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt
pip install pyinstaller

# Nettoyer les anciens builds
rm -rf build dist __pycache__

# Créer le répertoire bin dans src-tauri
mkdir -p src-tauri/bin

# Build avec PyInstaller
echo "📦 Compilation avec PyInstaller..."
pyinstaller --onefile \
    --name gabon_edu_backend \
    --hidden-import=uvicorn \
    --hidden-import=fastapi \
    --hidden-import=sqlalchemy \
    --hidden-import=aiosqlite \
    --hidden-import=pydantic \
    --hidden-import=jwt \
    --hidden-import=passlib \
    --hidden-import=argon2 \
    --hidden-import=pyotp \
    --hidden-import=qrcode \
    --hidden-import=weasyprint \
    --hidden-import=openpyxl \
    --add-data="backend:backend" \
    backend/main.py

# Copier l'exécutable dans src-tauri/bin
if [ "$(uname)" == "Darwin" ]; then
    cp dist/gabon_edu_backend src-tauri/bin/gabon_edu_backend
elif [ "$(uname)" == "Linux" ]; then
    cp dist/gabon_edu_backend src-tauri/bin/gabon_edu_backend
else
    cp dist/gabon_edu_backend.exe src-tauri/bin/gabon_edu_backend.exe
fi

echo "✅ Sidecar build terminé avec succès!"
echo "📁 Exécutable disponible dans: src-tauri/bin/"

# Nettoyer les fichiers temporaires
rm -rf build dist gabon_edu_backend.spec

echo "🎉 Prêt pour le build Tauri!"
