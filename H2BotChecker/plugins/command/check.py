from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.gates.b3auth import brn
import re
import asyncio
from datetime import datetime

@Client.on_message(filters.command("check"))
async def check_command(client: Client, message: Message):
    try:
        # Obtener el texto del mensaje
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("❌ Formato incorrecto. Usa: /check <cc|mm|yy|cvv>")
            return

        # Extraer datos de la tarjeta
        card_data = text[1]
        if "|" in card_data:
            cc, mes, ano, cvv = card_data.split("|")
        else:
            await message.reply_text("❌ Formato incorrecto. Usa: /check <cc|mm|yy|cvv>")
            return

        # Validar formato de la tarjeta
        if not re.match(r'^\d{16}$', cc):
            await message.reply_text("❌ Número de tarjeta inválido")
            return
        if not re.match(r'^\d{2}$', mes) or not 1 <= int(mes) <= 12:
            await message.reply_text("❌ Mes inválido")
            return

        # Validar año (acepta 2 o 4 dígitos)
        if not re.match(r'^\d{2,4}$', ano):
            await message.reply_text("❌ Año inválido")
            return
        
        # Convertir año a 2 dígitos si es necesario
        if len(ano) == 4:
            ano = ano[2:]
        
        # Validar que el año no sea anterior al actual
        current_year = datetime.now().year % 100
        if int(ano) < current_year:
            await message.reply_text("❌ Tarjeta expirada")
            return

        if not re.match(r'^\d{3,4}$', cvv):
            await message.reply_text("❌ CVV inválido")
            return

        # Obtener proxy (si existe)
        proxy = None
        if len(text) > 2:
            proxy = text[2]

        # Enviar mensaje de inicio
        status_msg = await message.reply_text("🔄 Verificando tarjeta...")

        # Ejecutar la verificación
        start_time = asyncio.get_event_loop().time()
        msg, respuesta = await brn(client, status_msg, cc, mes, ano, cvv, proxy)
        end_time = asyncio.get_event_loop().time()
        tiempo = round(end_time - start_time, 2)

        # Obtener información del BIN
        bin_info = f"{cc[:6]} - MEXICO 🇲🇽"  # Aquí podrías agregar una función para obtener más info del BIN

        # Formatear respuesta
        response = f"""あ » H2 Bot Checker | B3Auth

【𝘾𝙖𝙧𝙙】: {cc}|{mes}|{ano}|{cvv}
【𝙄𝙣𝙛𝙤 𝘽𝙄𝙉】: {bin_info}
【𝘽𝙖𝙣𝙠】: BANCO SANTANDER, S.A,
【𝙏𝙮𝙥𝙚】: MASTERCARD - CIRRUS - DEBIT
【𝙎𝙩𝙖𝙩 𝙪𝙨】: {msg}
【𝙍𝙚𝙨𝙥𝙪𝙚𝙨𝙩𝙖】: {respuesta}
【𝙏𝙞𝙢𝙚】: {tiempo}s
【𝙋𝙧𝙤𝙭𝙮】: {proxy if proxy else 'No proxy'} {'✅' if proxy else '❌'}
【𝙐𝙨𝙚𝙧】: @{message.from_user.username if message.from_user.username else message.from_user.id}
—————— あ » H2 Bot Checker ——————"""

        # Actualizar mensaje con el resultado
        await status_msg.edit_text(response)

    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}") 