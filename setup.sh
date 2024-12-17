#!/bin/bash

# Skrypt do instalacji i uruchomienia FastAPI (backend) i Vue.js (frontend) na WSL

set -e

# Zmienne dla sciezek
FASTAPI_DIR="$HOME/oscylatory-backend"
VUE_DIR="$HOME/oscylatory-frontend"

# Funkcja instalacji Node.js i npm (opcjonalnie)
install_node() {
    echo "Instalacja Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
}

# Funkcja instalacji Python3 i pip (opcjonalnie)
install_python() {
    echo "Instalacja Python3 i pip..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
}

# Uruchomienie FastAPI Backend
deploy_fastapi() {
    echo "\n[1/2] Uruchamianie FastAPI Backend...\n"
    cd $FASTAPI_DIR

    # Tworzenie wirtualnego srodowiska, jesli nie istnieje
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install fastapi uvicorn
        pip install scipy
        pip install numpy
        pip install pydantic
    else
        source venv/bin/activate
    fi

    # Uruchamianie FastAPI na porcie 8000
    nohup uvicorn api:app --host 0.0.0.0 --port 8000 &
    echo "FastAPI uruchomiony na porcie 8000!"
}

# Uruchomienie Vue.js Frontend
deploy_vue() {
    echo "\n[2/2] Uruchamianie Vue.js Frontend...\n"
    cd $VUE_DIR

    # Sprawdzenie czy node_modules istnieje
    if [ ! -d "node_modules" ]; then
        echo "Instalacja zaleznosci dla Vue.js..."
        npm install
    fi

    # Uruchamianie Vue.js na porcie 8080
    nohup npm run serve -- --host 0.0.0.0 &
    echo "Vue.js uruchomiony na porcie 8080!"
}

# Glowny skrypt
main() {
    echo "Rozpoczynam konfiguracje..."
    # Instalacja wymaganych narzedzi
    if ! command -v node &> /dev/null; then install_node; fi
    if ! command -v python3 &> /dev/null; then install_python; fi

    install_python
    deploy_fastapi

    install_node
    deploy_vue

    echo "\nBackend FastAPI: http://localhost:8000"
    echo "Frontend Vue.js: http://localhost:8080"
    echo "\nAplikacja uruchomiona pomyslnie!"
}

main