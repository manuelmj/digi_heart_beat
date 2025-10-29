#!/bin/bash
# --------------------------------------------
# Script para comprimir un archivo/carpeta y enviarlo por SCP
# Autor: Manuel Manjarres
# Fecha: 2025-10-15
# --------------------------------------------

# --- CONFIGURACIÓN ---
REMOTE_USER="$1"             # Usuario remoto
REMOTE_HOST="$2"             # IP o dominio remoto
LOCAL_PATH="src"             # Archivo o carpeta a comprimir
REMOTE_PATH="/tmp/"          # Carpeta destino en el servidor remoto
ARCHIVE_NAME="digi_heartbeat".tar.gz
INSTALLER_SCRIPT="install_digi_heartbeat.sh"
STARTER_SCRIPT="heartbeat_start.sh"

# --- VALIDACIÓN DE PARÁMETROS ---
if [ $# -lt 2 ]; then
    echo "Uso: $0  <usuario_remoto> <host_remoto> "
    exit 1
fi

# --- COMPRESIÓN ---
echo "🔹 Comprimiendo $LOCAL_PATH en $ARCHIVE_NAME ..."
tar -czf "$ARCHIVE_NAME" -C "$(dirname "$LOCAL_PATH")" "$(basename "$LOCAL_PATH")"

if [ $? -ne 0 ]; then
    echo "❌ Error al comprimir el archivo."
    exit 2
fi

mv "$ARCHIVE_NAME" packages/


DIR_TO_SEND="packages"
cp "$INSTALLER_SCRIPT" "$DIR_TO_SEND/"
cp "$STARTER_SCRIPT" "$DIR_TO_SEND/"

# --- ENVÍO POR SCP ---
echo "🚀 Enviando $DIR_TO_SEND a $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH ..."
scp -r "$DIR_TO_SEND" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"

if [ $? -ne 0 ]; then
    echo "❌ Error al enviar el archivo al servidor remoto."
    exit 3
fi

echo "✅ Archivo enviado exitosamente."


exit 0
