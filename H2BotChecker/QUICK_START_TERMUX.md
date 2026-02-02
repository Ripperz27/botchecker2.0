# ⚡ Inicio Rápido para Termux

Guía rápida para ejecutar el bot en Termux cuando está en GitHub.

## 🚀 Pasos Rápidos

### 1. Clonar desde GitHub

```bash
cd ~
git clone [TU_URL_DE_GITHUB] H2BotChecker
cd H2BotChecker
```

**Ejemplo:**
```bash
git clone https://github.com/tu-usuario/H2BotChecker.git H2BotChecker
cd H2BotChecker
```

### 2. Instalación Automática

```bash
chmod +x install_termux.sh
bash install_termux.sh
```

El script te preguntará:
- Si quieres clonar desde GitHub o usar archivos locales
- Si quieres editar `main.py` para configurar tus credenciales

### 3. Configurar Credenciales

Edita `main.py` y configura:
- `api_id` - Tu API ID de Telegram
- `api_hash` - Tu API Hash de Telegram  
- `bot_token` - El token de tu bot (de @BotFather)

```bash
nano main.py
```

Busca estas líneas y reemplázalas:
```python
api_id=TU_API_ID
api_hash='TU_API_HASH'
bot_token='TU_BOT_TOKEN'
```

Para guardar en nano:
- `Ctrl + O` → Enter → `Ctrl + X`

### 4. Ejecutar el Bot

**En primer plano:**
```bash
bash start_bot.sh
```

**En segundo plano (recomendado):**
```bash
bash start_bot_background.sh
```

## 📋 Comandos Útiles

### Ver logs del bot (si está en segundo plano)
```bash
tail -f bot.log
```

### Detener el bot
```bash
pkill -f "python main.py"
```

### Verificar que el bot está corriendo
```bash
pgrep -f "python main.py"
```

### Reiniciar el bot
```bash
pkill -f "python main.py"
bash start_bot_background.sh
```

## 🔄 Actualizar desde GitHub

Si actualizaste el código en GitHub:

```bash
cd ~/H2BotChecker
git pull
source venv/bin/activate
pip install -r requirements.txt
```

## ⚠️ Solución Rápida de Problemas

**Error: "command not found"**
```bash
pkg install python git -y
```

**Error al instalar dependencias**
```bash
pkg install python-dev clang -y
pip install --upgrade pip
pip install -r requirements.txt
```

**El bot no inicia**
- Verifica tus credenciales en `main.py`
- Asegúrate de tener internet
- Revisa los logs: `cat bot.log`

## 📱 Mantener el Bot Activo

1. **Desactivar optimización de batería:**
   - Configuración → Aplicaciones → Termux → Batería
   - Selecciona "Sin restricciones"

2. **No cerrar Termux completamente:**
   - Solo minimízalo, no lo cierres

3. **Usar Wake Lock:**
```bash
pkg install termux-api -y
termux-wake-lock
```

## ✅ Verificación

Para verificar que todo funciona:

```bash
# Verificar dependencias
python check_termux.py

# Probar el bot
python main.py
```

Si ves "Bot corriendo..." sin errores, ¡está listo! 🎉

---

**¿Necesitas más ayuda?** Consulta la [Guía Completa](TERMUX.md)

