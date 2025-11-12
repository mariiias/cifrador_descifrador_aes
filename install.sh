#!/bin/bash

REQUIRED="3.10"
COL_ERROR=$'\e[97;41;1m' # Letras blancas, fondo rojo, bold
COL_OK=$'\e[97;42;1m'    # Letras blancas, fondo verde, bold
NC=$'\e[0m'              # Reset

if ! command -v python3 &> /dev/null; then
    echo -e "${COL_ERROR} python3 no está instalado. ${NC}"
    echo -e "${COL_ERROR} Instálalo con: sudo apt install python3.10 ${NC}"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo -e "${COL_ERROR} pip no está instalado. ${NC}"
    echo -e "${COL_ERROR} Instálalo con: sudo apt install python3-pip ${NC}"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

if [[ "$(printf '%s\n' "$REQUIRED" "$PY_VERSION" | sort -V | head -n1)" != "$REQUIRED" ]]; then
    echo -e "${COL_ERROR} Se requiere Python >= $REQUIRED. Tienes Python $PY_VERSION. ${NC}"    
    exit 1
fi

echo -e "${COL_OK} Python $PY_VERSION detectado. Continuando... ${NC}"

echo -e ">> Verificando que el módulo ensurepip esté disponible..."
if ! python3 -m ensurepip --version &> /dev/null; then
    echo -e "${COL_ERROR} El módulo ensurepip no está disponible. No se puede crear el entorno virtual. ${NC}"
    echo -e "${COL_ERROR} Asegúrate de tener instalado el paquete 'python3.10-venv'. ${NC}"
    exit 1
fi

echo -e "${COL_OK} Módulo ensurepip detectado. Continuando... ${NC}"


echo -e ">> Creando entorno virtual 'venv'..."
python3.10 -m venv venv || { echo "${COL_ERROR} Error al crear el entorno virtual ${NC}"; exit 1; }

echo -e "${COL_OK} Entorno virtual creado. Continuando... ${NC}"

echo -e ">> Activando entorno virtual..."
source venv/bin/activate || { echo "${COL_ERROR} Error al activar el entorno virtual ${NC}"; exit 1; }

echo -e "${COL_OK} Entorno virtual activado. Continuando... ${NC}"

echo -e ">> Actualizando pip..."
pip install --upgrade pip

echo -e "${COL_OK} pip actualizado. Continuando... ${NC}"

echo -e ">> Instalando dependencias..."
pip install -r requirements.txt || { echo "${COL_ERROR} Error al instalar dependencias ${NC}"; exit 1; }

echo -e "${COL_OK} Dependencias instaladas. Continuando... ${NC}"

echo -e ">> Dando permisos de ejecución a 'xaes.py'..."
chmod +x xaes.py || { echo "${COL_ERROR} Error al dar permisos a xaes.py ${NC}"; exit 1; }

echo -e "${COL_OK} Instalación completa. ${NC}"
echo -e "Para ejecutar el programa, sigue estos pasos:"
echo -e "1. Activa el entorno virtual: source venv/bin/activate"
echo -e "2. Ejecuta el programa: cat archivo.txt | ./xaes.py -e \"clave\" > archivo.enc"
echo -e "3. Para salir del entorno virtual, usa: deactivate"
