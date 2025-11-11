#!bin/bash 

# ================================
# CONFIGURACIÓN - VARIABLES DE RUTAS
# ================================
# Rutas de archivos y directorios
# DIGI_PATH="/etc/config/scripts/"
DIGI_OPT_PATH="/opt/custom"
DIGI_PATH_HEARTBEAT="${DIGI_OPT_PATH}/digi_heartbeat/main.py"

# ================================
python ${DIGI_PATH_HEARTBEAT}
# ================================

if [ $? -ne 0 ]; then
    echo "❌ Error al iniciar Digi Heartbeat."
    exit 1
fi
echo "✅ Digi Heartbeat iniciado correctamente."
