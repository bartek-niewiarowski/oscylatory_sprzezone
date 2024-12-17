#!/bin/bash

# Skrypt do instalacji i uruchomienia FastAPI (backend) i Vue.js (frontend) na WSL

set -e

# Zmienne dla sciezek
FASTAPI_DIR="$HOME/oscylatory_sprzezone/oscylatory-backend"
VUE_DIR="$HOME/oscylatory_sprzezone/oscylatory-frontend"

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
    fi
    . venv/bin/activate

    # Instalacja wymaganych pakietow
    pip install --upgrade pip
    pip install fastapi uvicorn scipy numpy pydantic

    # Sprawdzenie pelnej sciezki do uvicorn
    UVICORN_PATH=$(which uvicorn)
    echo "Uvicorn znaleziony: $UVICORN_PATH"

    # Uruchamianie FastAPI na porcie 8000
    nohup $UVICORN_PATH api:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
    sleep 2
    if pgrep -f "$UVICORN_PATH api:app" > /dev/null; then
        echo "FastAPI uruchomiony na porcie 8000! Log zapisany w fastapi.log."
    else
        echo "Nie udalo sie uruchomic FastAPI. Sprawdz fastapi.log."
        exit 1
    fi
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

    # Sprawdzenie i instalacja vue-cli-service, jesli nie istnieje
    if ! npx vue-cli-service --version &> /dev/null; then
        echo "vue-cli-service nie znaleziono, instalacja lokalna..."
        npm install @vue/cli-service --save-dev
    fi

    # Uruchamianie Vue.js na porcie 8080
    nohup npx vue-cli-service serve --host 0.0.0.0 > vue.log 2>&1 &
    sleep 2
    if pgrep -f "vue-cli-service serve" > /dev/null; then
        echo "Vue.js uruchomiony na porcie 8080! Log zapisany w vue.log."
    else
        echo "Nie udalo sie uruchomic Vue.js. Sprawdz vue.log."
        exit 1
    fi
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
    echo "\nAby zatrzymac aplikacje, uzyj komend: 'pkill -f uvicorn' oraz 'pkill -f vue-cli-service'."
}

main