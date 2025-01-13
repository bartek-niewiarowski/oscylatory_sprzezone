#!/bin/bash

set -e

# Ścieżka do folderu z backendem- FastAPI
FASTAPI_DIR="oscylatory-backend"

# Ścieżka do folderu z frontendem- Vue.js
VUE_DIR="../oscylatory-frontend"

# funckja do wykrywania systemu operacyjnego
detect_os() {
    local unameOut
    unameOut="$(uname -s)"

    # Darwin => MacOS
    # Linux => Linux (dodatkowo sprawdzamy czy Ubuntu)
    case "${unameOut}" in
        Linux*)
            if command -v lsb_release &>/dev/null; then
                local distro
                distro="$(lsb_release -is)"
                if [ "${distro}" = "Ubuntu" ]; then
                    OS="ubuntu"
                else
                    echo "Twoj linux to nie ubuntu. Skrypt setup.sh moze nie dzialac prawidlowo."
                    OS="other_linux"
                fi
            else
                echo "lsb_release nie znaleziono, nie mozna okreslic dystrybucji linuxa."
                echo "Kontynuuowanie jako dystrybucja inna niz Ubuntu."
                OS="other_linux"
            fi
            ;;
        Darwin*)
            OS="macos"
            ;;
        *)
            echo "Uzywasz niewspieranego systemu operacyjnego: ${unameOut}"
            echo "Wychodzenie."
            exit 1
            ;;
    esac

    echo "Wykryty system operacyjny: $OS"
}


#instalacja node.js i pythona na ubuntu
install_node_ubuntu() {
    echo "Instalowanie Node.js na Ubuntu..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
}

install_python_ubuntu() {
    echo "Instalowanie Python3 i pip na Ubuntu..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
}


#instalacja node.js i pythona na macos
install_node_macos() {
    echo "Instalowanie Node.js na macOS uzywajac Homebrew..."
    brew update
    brew install node
}

install_python_macos() {
    echo "Instalowanie Python3 na macOS uzywajac Homebrew..."
    brew update
    brew install python
}


#deployment backendu FastAPI
deploy_fastapi() {
    echo -e "\n[1/2] Uruchamianie backendu FastAPI...\n"
    cd "$FASTAPI_DIR"

    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    source venv/bin/activate

    pip install --upgrade pip
    pip install fastapi uvicorn scipy numpy pydantic

    UVICORN_PATH=$(which uvicorn)
    echo "Uvicorn znaleziony: $UVICORN_PATH"

    nohup "$UVICORN_PATH" api:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 &
    sleep 2

    if pgrep -f "$UVICORN_PATH api:app" > /dev/null; then
        echo "FastAPI uruchomiony na porcie 8000! Log: fastapi.log"
    else
        echo "Nie udalo sie uruchomic FastAPI. Sprawdz fastapi.log."
        exit 1
    fi
}


# deployment frontendu Vue.js
deploy_vue() {
    echo -e "\n[2/2] Uruchamianie frontendu Vue.js...\n"
    cd "$VUE_DIR"

    if [ ! -d "node_modules" ]; then
        echo "Instalowanie zaleznosci Vue.js..."
        npm install
    fi

    if ! npx vue-cli-service --version &> /dev/null; then
        echo "vue-cli-service nie znaleziony, instalowanie..."
        npm install @vue/cli-service --save-dev
    fi

    nohup npx vue-cli-service serve --host 0.0.0.0 --port 8080 > vue.log 2>&1 &
    sleep 2

    if pgrep -f "vue-cli-service serve" > /dev/null; then
        echo "Vue.js uruchomiony na porcie 8080! Log: vue.log"
    else
        echo "Nie udalo sie uruchomic Vue.js. Sprawdz vue.log."
        exit 1
    fi
}


main() {
    detect_os

    if [ "$OS" = "macos" ]; then
        if ! command -v brew &> /dev/null; then
            echo "Homebrew nie jest zainstalowany. Zainstaluj homebrew."
            exit 1
        fi

        if ! command -v node &> /dev/null; then
            install_node_macos
        else
            echo "Node.js jest juz zainstalowany (macOS)."
        fi

        if ! command -v python3 &> /dev/null; then
            install_python_macos
        else
            echo "Python3 jest juz zainstalowany (macOS)."
        fi

    elif [ "$OS" = "ubuntu" ]; then
        if ! command -v node &> /dev/null; then
            install_node_ubuntu
        else
            echo "Node.js jest juz zainstalowany (Ubuntu)."
        fi

        if ! command -v python3 &> /dev/null; then
            install_python_ubuntu
        else
            echo "Python3 jest juz zainstalowany (Ubuntu)."
        fi

    else
        echo "Skrypt nie wspiera instalacji zaleznosci na '$OS'."
        echo "Mozesz recznie zainstalowac wszystkie zaleznosci."
    fi

    deploy_fastapi
    deploy_vue

    echo -e "\nFastAPI backend: http://localhost:8000"
    echo "Vue.js frontend: http://localhost:8080"
    echo -e "\nAplikacja poprawnie uruchomiona!"
    echo "Aby zatrzymac uzyj komend:"
    echo "  pkill -f uvicorn"
    echo "  pkill -f vue-cli-service"
}

main
