# 🚀 Guía de Instalación para Termux (Android)

Esta guía te ayudará a instalar y ejecutar el bot H2 Bot Checker en Termux, manteniendo todas sus funcionalidades.

## 📋 Requisitos Previos

- Android 7.0 o superior
- Termux instalado desde [F-Droid](https://f-droid.org/en/packages/com.termux/) (NO desde Play Store)
- Conexión a internet estable
- Cuenta de Telegram
- API ID y API Hash de Telegram (obtenidos de https://my.telegram.org)

## 🔧 Instalación Paso a Paso

### ⚡ Instalación Rápida (Recomendada)

Si el bot está en GitHub, usa el script de instalación automática:

```bash
# 1. Clonar el repositorio
cd ~
git clone [URL_DE_TU_REPOSITORIO_GITHUB] H2BotChecker
cd H2BotChecker

# 2. Dar permisos de ejecución al script
chmod +x install_termux.sh

# 3. Ejecutar el instalador automático
bash install_termux.sh
```

El script instalará todo automáticamente y te guiará en la configuración.

### 📝 Instalación Manual

Si prefieres hacerlo manualmente o el script no funciona:

#### 1. Instalar Termux y Dependencias

Abre Termux y ejecuta los siguientes comandos uno por uno:

```bash
# Actualizar paquetes
pkg update && pkg upgrade -y

# Instalar Python y herramientas necesarias
pkg install python -y
pkg install git -y
pkg install wget -y
pkg install proot -y

# Instalar pip si no viene incluido
python -m ensurepip --upgrade
```

#### 2. Clonar el Bot desde GitHub

**Si tienes el bot en GitHub (RECOMENDADO):**
```bash
cd ~
git clone [URL_DE_TU_REPOSITORIO_GITHUB] H2BotChecker
cd H2BotChecker
```

**Ejemplo:**
```bash
git clone https://github.com/tu-usuario/H2BotChecker.git H2BotChecker
cd H2BotChecker
```

**Opción B: Si tienes los archivos en tu teléfono**
```bash
# Los archivos deben estar en la carpeta Downloads o en storage
cd ~
mkdir H2BotChecker
cd H2BotChecker
# Usa un explorador de archivos para copiar los archivos del bot aquí
# O usa termux-setup-storage para acceder a la carpeta Downloads
```

**Opción C: Usar termux-setup-storage (Recomendado)**
```bash
# Permitir acceso a almacenamiento
termux-setup-storage

# Copiar archivos desde Downloads
cd ~/storage/downloads
# Si tienes el bot comprimido aquí, descomprímelo primero
cd ~
cp -r storage/downloads/H2BotChecker ./
cd H2BotChecker
```

### 3. Configurar el Bot

Edita el archivo `main.py` con tus credenciales:

```bash
# Instalar un editor de texto (nano es más fácil)
pkg install nano -y

# Editar main.py
nano main.py
```

Busca estas líneas y reemplázalas con tus credenciales:
```python
api_id=TU_API_ID        # Reemplaza con tu API ID
api_hash='TU_API_HASH'  # Reemplaza con tu API Hash
bot_token='TU_BOT_TOKEN' # Reemplaza con tu Bot Token
```

Para guardar en nano:
- Presiona `Ctrl + O` para guardar
- Presiona `Enter` para confirmar
- Presiona `Ctrl + X` para salir

### 4. Crear Entorno Virtual (Opcional pero Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Deberías ver (venv) al inicio de la línea
```

### 5. Instalar Dependencias

```bash
# Asegúrate de estar en la carpeta del bot
cd ~/H2BotChecker

# Si creaste el entorno virtual, actívalo primero
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Nota:** Si alguna dependencia falla, intenta instalar las dependencias del sistema primero:
```bash
pkg install python-dev clang -y
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 6. Ejecutar el Bot

**Opción A: Usando el script de inicio (Recomendado)**
```bash
cd ~/H2BotChecker
chmod +x start_bot.sh
bash start_bot.sh
```

**Opción B: Manualmente**
```bash
# Asegúrate de estar en la carpeta del bot
cd ~/H2BotChecker

# Si usas entorno virtual, actívalo
source venv/bin/activate

# Ejecutar el bot
python main.py
```

El bot debería iniciar y mostrar "Bot corriendo...". Si ves errores, revisa la sección de solución de problemas.

## 🔄 Ejecutar el Bot en Segundo Plano

Para que el bot siga corriendo incluso cuando cierres Termux:

### Opción 1: Usar el script automático (Más Fácil)

```bash
cd ~/H2BotChecker
chmod +x start_bot_background.sh
bash start_bot_background.sh
```

Este script iniciará el bot en segundo plano y te mostrará cómo ver los logs y detenerlo.

### Opción 2: Usar `nohup` (Simple)

```bash
cd ~/H2BotChecker
source venv/bin/activate  # Si usas entorno virtual
nohup python main.py > bot.log 2>&1 &
```

Para ver los logs:
```bash
tail -f bot.log
```

Para detener el bot:
```bash
pkill -f "python main.py"
```

### Opción 2: Usar `tmux` (Recomendado)

```bash
# Instalar tmux
pkg install tmux -y

# Crear una sesión nueva
tmux new -s bot

# Dentro de tmux, ejecuta el bot
cd ~/H2BotChecker
source venv/bin/activate  # Si usas entorno virtual
python main.py
```

Para salir de tmux sin detener el bot:
- Presiona `Ctrl + B`, luego `D`

Para volver a la sesión:
```bash
tmux attach -t bot
```

Para detener el bot:
- Entra a la sesión con `tmux attach -t bot`
- Presiona `Ctrl + C` para detener el bot
- Escribe `exit` para cerrar la sesión

### Opción 3: Usar `termux-boot` (Inicio Automático)

```bash
# Instalar termux-boot
pkg install termux-services -y

# Crear script de inicio
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-bot.sh
```

Pega este contenido en el script:
```bash
#!/data/data/com.termux/files/usr/bin/bash
cd ~/H2BotChecker
source venv/bin/activate
python main.py
```

Hacer el script ejecutable:
```bash
chmod +x ~/.termux/boot/start-bot.sh
```

**Nota:** El bot se iniciará automáticamente cuando Termux se inicie.

## 📝 Comandos Disponibles del Bot

Una vez que el bot esté corriendo, puedes usar estos comandos en Telegram:

- `/start` - Inicia el bot y muestra el menú de bienvenida
- `/cmds` - Muestra el menú principal con todas las opciones
- `/bin` - Obtiene información de un BIN (formato: `/bin xxxxxx`)
- `/gen` - Genera tarjetas (formato: `/gen xxxxxx`)
- `/reset` - Reinicia tu perfil/configuración

## 🛠️ Solución de Problemas

### Error: "python: command not found"
```bash
pkg install python -y
```

### Error al instalar dependencias
```bash
# Actualizar pip y herramientas
pip install --upgrade pip setuptools wheel
pkg install python-dev clang -y

# Intentar instalar de nuevo
pip install -r requirements.txt
```

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error de conexión o API
- Verifica que tu API_ID, API_HASH y BOT_TOKEN sean correctos
- Asegúrate de tener conexión a internet
- Verifica que el bot no esté bloqueado en Telegram

### El bot se detiene al cerrar Termux
- Usa `tmux` o `nohup` como se explicó arriba
- No cierres Termux completamente, solo minimízalo

### Error de permisos
```bash
# Dar permisos de ejecución
chmod +x main.py
```

### Limpiar e reinstalar todo
```bash
cd ~
rm -rf H2BotChecker
# Sigue los pasos de instalación desde el principio
```

## 📱 Mantener Termux Activo

Para evitar que Android mate el proceso de Termux:

1. **Desactivar optimización de batería para Termux:**
   - Configuración → Aplicaciones → Termux → Batería
   - Selecciona "Sin restricciones" o "No optimizar"

2. **Mantener Termux en segundo plano:**
   - No cierres Termux completamente
   - Solo minimízalo

3. **Usar Wake Lock (Opcional):**
```bash
pkg install termux-api -y
termux-wake-lock
```

## 🔒 Seguridad

- **NUNCA** compartas tu `api_id`, `api_hash` o `bot_token`
- Mantén tus credenciales seguras
- No subas el archivo `main.py` con tus credenciales a repositorios públicos

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del bot: `tail -f bot.log` (si usas nohup)
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de tener la última versión de Python y pip

## ✅ Verificación Final

Para verificar que todo funciona:

1. El bot debe iniciar sin errores
2. Debes poder enviar `/start` al bot en Telegram
3. El bot debe responder con el mensaje de bienvenida
4. El comando `/cmds` debe mostrar el menú principal

¡Listo! Tu bot debería estar funcionando perfectamente en Termux con todas sus funcionalidades. 🎉

