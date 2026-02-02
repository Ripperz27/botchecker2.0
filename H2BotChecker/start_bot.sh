#!/data/data/com.termux/files/usr/bin/bash
# Script para iniciar el bot en Termux
# Uso: bash start_bot.sh

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si estamos en la carpeta correcta
if [ ! -f "main.py" ]; then
    print_error "No se encontró main.py"
    print_info "Navegando a ~/H2BotChecker..."
    cd ~/H2BotChecker 2>/dev/null || {
        print_error "No se encontró la carpeta H2BotChecker"
        print_info "Asegúrate de estar en la carpeta del bot o ejecuta:"
        print_info "cd ~/H2BotChecker"
        exit 1
    }
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    print_info "Activando entorno virtual..."
    source venv/bin/activate
else
    print_error "No se encontró el entorno virtual"
    print_info "Ejecuta primero: bash install_termux.sh"
    exit 1
fi

# Verificar dependencias
print_info "Verificando dependencias..."
python -c "import pyrogram" 2>/dev/null || {
    print_error "Pyrogram no está instalado"
    print_info "Instalando dependencias..."
    pip install -r requirements.txt
}

print_info "Iniciando bot..."
echo ""
python main.py

