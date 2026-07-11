#!/bin/bash
set -e

echo "🚀 Démarrage de l'application FIFA Match Predictor"
echo ""

echo "📦 Vérification des dépendances..."
pip install -q -r requirements.txt 2>/dev/null

echo "🧠 Entraînement / chargement du modèle..."
cd "$(dirname "$0")"
python -c "from app.train import train_and_save; train_and_save()" 2>&1 | tail -5

echo ""
echo "🔧 Démarrage du backend FastAPI (port 8000)..."
uvicorn app.api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

sleep 3

echo "🎨 Démarrage du frontend Streamlit (port 8501)..."
streamlit run app/frontend.py --server.port 8501 --server.headless true &
FE_PID=$!

echo ""
echo "============================================"
echo "  ✅ Application prête !"
echo "  🔧 API :      http://localhost:8000"
echo "  📖 Docs API :  http://localhost:8000/docs"
echo "  🎨 Frontend :  http://localhost:8501"
echo "============================================"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter..."

trap "kill $API_PID $FE_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
