# H2 Bot Checker

Bot de Telegram para verificación de tarjetas y herramientas relacionadas.

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Telegram
- API ID y API Hash de Telegram (obtenidos de https://my.telegram.org)

## 📱 ¿Usando Termux (Android)?

Si quieres ejecutar este bot en Termux (Android):

- **🚀 Inicio Rápido:** Consulta la **[Guía Rápida para Termux](QUICK_START_TERMUX.md)** (recomendado si el bot está en GitHub)
- **📖 Guía Completa:** Consulta la **[Guía Completa de Termux](TERMUX.md)** para instrucciones detalladas

**Características:**
- ✅ Instalación automática con scripts
- ✅ Ejecución en segundo plano
- ✅ Compatible con GitHub (clonar y ejecutar)
- ✅ Mantiene todas las funcionalidades del bot

El bot es **completamente compatible con Termux** y mantiene todas sus funcionalidades.

## 🚀 Instalación Paso a Paso

1. **Preparación del entorno**
   - Descarga Python desde [python.org](https://www.python.org/downloads/)
   - Durante la instalación, marca la casilla "Add Python to PATH"
   - Reinicia tu computadora después de instalar Python

2. **Preparación del bot**
   - Extrae el archivo .zip del bot en tu escritorio
   - Renombra la carpeta extraída a "H2BotChecker" (opcional)
   - Abre el Explorador de Windows y navega hasta la carpeta

3. **Crear el bot en Telegram**
   - Abre Telegram y busca "@BotFather"
   - Inicia una conversación con /start
   - Envía el comando /newbot
   - Sigue las instrucciones:
     * Escribe un nombre para tu bot (ejemplo: "Mi Bot Checker")
     * Escribe un username para tu bot (debe terminar en 'bot', ejemplo: "mi_bot_checker_bot")
   - Guarda el TOKEN que te da BotFather (lo necesitarás después)

4. **Obtener API ID y API Hash**
   - Ve a https://my.telegram.org
   - Inicia sesión con tu número de teléfono
   - Ve a "API development tools"
   - Crea una nueva aplicación
   - Inventa todo lo que te pidan, lo importante es el API_ID y el API_HASH
   - Guarda el `api_id` y `api_hash`

5. **Configurar el bot**
   - Abre la carpeta del bot
   - Abre el archivo `main.py` con el Bloc de notas
   - Busca y reemplaza estas líneas:
     ```python
     api_id=TU_API_ID        # Reemplaza con el número que obtuviste
     api_hash='TU_API_HASH'  # Reemplaza con el hash que obtuviste
     bot_token='TU_BOT_TOKEN' # Reemplaza con el token de BotFather
     ```

6. **Crear entorno virtual**
   - Abre PowerShell o CMD
   - Navega hasta la carpeta del bot:
     ```bash
     cd Desktop\H2BotChecker
     ```
   - Crea el entorno virtual:
     ```bash
     python -m venv venv
     ```
   - Activa el entorno virtual:
     ```bash
     .\venv\Scripts\activate
     ```

7. **Instalar dependencias**
   - Con el entorno virtual activado, ejecuta:
     ```bash
     pip install -r requirements.txt
     ```

## 🏃‍♂️ Ejecución del Bot

1. **Iniciar el bot**
   - Asegúrate de que el entorno virtual esté activado (verás (venv) al inicio de la línea)
   - Ejecuta:
     ```bash
     python main.py
     ```
   - Deberías ver un mensaje indicando que el bot está corriendo

2. **Probar el bot**
   - Abre Telegram
   - Busca tu bot por el username que le diste
   - Envía el comando /start
   - El bot debería responder

## 📝 Comandos Disponibles

- `/start` - Inicia el bot
- `/cmds` - Despliega el menu y comandos disponibles de bot checker 
- `/bin` - Obtiene información de un BIN (formato: /bin xxxxxx)
- `/gen` - Genera tarjetas (formato: /gen xxxxxx)

## ⚠️ Notas Importantes

- Asegúrate de tener una conexión estable a internet
- El bot requiere permisos de administrador en los grupos donde se use
- Mantén tus credenciales seguras y no las compartas
- Si cierras la terminal, necesitarás activar el entorno virtual nuevamente

## 🛠️ Solución de Problemas

Si encuentras algún error:

1. **Error al instalar dependencias**
   - Asegúrate de que Python está en el PATH
   - Intenta ejecutar: `python -m pip install --upgrade pip`

2. **Error al iniciar el bot**
   - Verifica que las credenciales (api_id, api_hash, bot_token) sean correctas
   - Asegúrate de que el entorno virtual esté activado
   - Verifica tu conexión a internet

3. **El bot no responde**
   - Verifica que el bot esté corriendo en la terminal
   - Asegúrate de que el token del bot sea correcto
   - Intenta reiniciar el bot

## 📞 Soporte

Para soporte o reportar problemas, contacta a @soportecursos