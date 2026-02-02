#!/data/data/com.termux/files/usr/bin/bash
# Script para iniciar el bot en segundo plano usando nohup
# Uso: bash start_bot_background.sh

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
    cd ~/H2BotChecker 2>/dev/null || {
        print_error "No se encontró la carpeta del bot"
        exit 1
    }
fi

# Verificar si el bot ya está corriendo
if pgrep -f "python main.py" > /dev/null; then
    print_error "El bot ya está corriendo"
    print_info "Para detenerlo: pkill -f 'python main.py'"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

print_info "Iniciando bot en segundo plano..."
nohup python main.py > bot.log 2>&1 &

BOT_PID=$!
sleep 2

if ps -p $BOT_PID > /dev/null; then
    print_info "✅ Bot iniciado correctamente (PID: $BOT_PID)"
    print_info "📋 Ver logs en tiempo real: tail -f bot.log"
    print_info "🛑 Detener bot: pkill -f 'python main.py'"
    echo ""
    print_info "Mostrando últimas líneas del log:"
    tail -n 10 bot.log
else
    print_error "El bot no pudo iniciarse"
    print_info "Revisa el log: cat bot.log"
fi

