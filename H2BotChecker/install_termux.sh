#!/data/data/com.termux/files/usr/bin/bash
# Script de instalación automática para Termux
# Uso: bash install_termux.sh

echo "🚀 Instalador de H2 Bot Checker para Termux"
echo "=========================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si estamos en Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    print_error "Este script está diseñado para Termux (Android)"
    exit 1
fi

print_info "Actualizando paquetes..."
pkg update -y && pkg upgrade -y

print_info "Instalando dependencias del sistema..."
pkg install -y python git wget proot nano

print_info "Actualizando pip..."
python -m ensurepip --upgrade
pip install --upgrade pip setuptools wheel

print_info "Instalando herramientas de compilación (necesarias para algunas dependencias)..."
pkg install -y python-dev clang

print_info "Verificando Python..."
python_version=$(python --version 2>&1)
print_info "Versión de Python: $python_version"

# Preguntar si quiere instalar desde GitHub o usar archivos locales
echo ""
print_warn "¿Dónde está el código del bot?"
echo "1) En GitHub (clonar repositorio)"
echo "2) Ya está en esta carpeta"
read -p "Selecciona una opción (1 o 2): " option

if [ "$option" = "1" ]; then
    read -p "Ingresa la URL del repositorio de GitHub: " repo_url
    print_info "Clonando repositorio..."
    cd ~
    if [ -d "H2BotChecker" ]; then
        print_warn "La carpeta H2BotChecker ya existe. ¿Eliminarla? (s/n)"
        read -p "> " confirm
        if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
            rm -rf H2BotChecker
        else
            print_error "Instalación cancelada"
            exit 1
        fi
    fi
    git clone "$repo_url" H2BotChecker
    cd H2BotChecker
elif [ "$option" = "2" ]; then
    print_info "Usando archivos locales..."
    if [ ! -f "main.py" ]; then
        print_error "No se encontró main.py en el directorio actual"
        print_error "Asegúrate de estar en la carpeta del bot"
        exit 1
    fi
else
    print_error "Opción inválida"
    exit 1
fi

print_info "Creando entorno virtual..."
python -m venv venv

print_info "Activando entorno virtual..."
source venv/bin/activate

print_info "Instalando dependencias de Python..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    print_error "No se encontró requirements.txt"
    exit 1
fi

print_info "Verificando instalación..."
python check_termux.py

echo ""
print_info "✅ Instalación completada!"
echo ""
print_warn "IMPORTANTE: Antes de ejecutar el bot, debes:"
echo "1. Editar main.py y configurar tus credenciales:"
echo "   - api_id"
echo "   - api_hash"
echo "   - bot_token"
echo ""
echo "2. Para ejecutar el bot:"
echo "   cd ~/H2BotChecker"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
print_info "¿Quieres abrir main.py ahora para configurarlo? (s/n)"
read -p "> " edit_now

if [ "$edit_now" = "s" ] || [ "$edit_now" = "S" ]; then
    print_info "Abriendo main.py con nano..."
    print_warn "Busca las líneas con api_id, api_hash y bot_token"
    print_warn "Presiona Ctrl+O para guardar, Enter para confirmar, Ctrl+X para salir"
    sleep 3
    nano main.py
fi

echo ""
print_info "🎉 ¡Listo! El bot está instalado."
print_info "Ejecuta 'bash start_bot.sh' para iniciar el bot"

