from pyrogram import filters, Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import re
from .luhn_gen import Generator
from pyrogram.errors import FloodWait
import asyncio

@Client.on_callback_query(filters.regex("^exit$"))
async def exit(client: Client, callback_query: CallbackQuery):
    try:
        # Obtener el texto del mensaje
        message_text = callback_query.message.text
        
        # Buscar el BIN en el mensaje usando regex
        bin_match = re.search(r'荣 Bin -» <code>(\d+)</code>', message_text)
        if not bin_match:
            await callback_query.answer("❌ No se pudo encontrar el BIN", show_alert=True)
            return
            
        bin_number = bin_match.group(1)
        
        # Obtener información del BIN
        binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_number[:6]}')
        if binreq.status_code != 200:
            await callback_query.answer("❌ Error al obtener información del BIN", show_alert=True)
            return
            
        bin_data = binreq.json()
        
        # Construir el mensaje con la información del BIN
        message = f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙄𝙣𝙛𝙤 𝘽𝙞𝙣】:
荣 Bin -» <code>{bin_number[:6]}</code>
荣 Type -» {bin_data.get('type', 'Unknown')}
荣 Level -» {bin_data.get('level', 'Unknown')}
荣 Bank -» {bin_data.get('bank', 'Unknown')}
荣 Country -» {bin_data.get('country', 'Unknown')}
━━━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Información obtenida exitosamente ✅
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""

        await callback_query.edit_message_text(message)
        await callback_query.answer("✅ Información del BIN obtenida")
        
    except FloodWait as e:
        await callback_query.answer(
            f"⚠️ Por favor espera {e.value} segundos antes de intentar nuevamente",
            show_alert=True
        )
    except Exception as e:
        print(f"Error en exit callback: {str(e)}")
        await callback_query.answer("❌ Error al obtener información del BIN", show_alert=True)

@Client.on_callback_query(filters.regex("^regen:"))
async def regen_cc(client: Client, callback_query: CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[1])
        
        if callback_query.from_user.id != user_id:
            await callback_query.answer("❌ Solo el usuario que generó las CCs puede regenerarlas", show_alert=True)
            return

        # Obtener el BIN del mensaje original
        message_text = callback_query.message.text
        bin_match = re.search(r'Format: (\d+)', message_text)
        if not bin_match:
            await callback_query.answer("❌ No se pudo encontrar el BIN", show_alert=True)
            return
            
        bin_number = bin_match.group(1)
        
        # Verificar el BIN
        binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_number[:6]}')
        if 'Invalid BIN' in binreq.text:
            await callback_query.answer("❌ BIN inválido", show_alert=True)
            return
        elif 'not found' in binreq.text:
            await callback_query.answer("❌ BIN no encontrado", show_alert=True)
            return
            
        # Extraer las fechas originales del mensaje
        fechas = []
        bins = []
        for line in message_text.split('\n'):
            match = re.search(r'<code>(\d{6,16})\|(\d{2})\|(\d{2,4})\|\w+</code>', line)
            if match:
                bins.append(match.group(1)[:6])
                fechas.append((match.group(2), match.group(3)))
        extra = []
        if fechas:
            # Si hay fechas, mantenerlas
            for idx, (mes, ano) in enumerate(fechas):
                bin6 = bins[idx] if idx < len(bins) else bin_number[:6]
                # Generar solo número y cvv
                cc_cvv = Generator(bin6, 1, True).generate_ccs()[0]
                cc, _, _, cvv = cc_cvv.split('|')
                extra.append(f"{cc}|{mes}|{ano}|{cvv}")
        else:
            # Si no hay fechas, generar tarjetas completas aleatorias
            extra = Generator(bin_number[:6], 10, True).generate_ccs()
        
        # Construir el mensaje
        texto = f'''<b>Generador ccs

Format: {bin_number}

<code>{extra[0]}</code>
<code>{extra[1]}</code>
<code>{extra[2]}</code>
<code>{extra[3]}</code>
<code>{extra[4]}</code>
<code>{extra[5]}</code>
<code>{extra[6]}</code>
<code>{extra[7]}</code>
<code>{extra[8]}</code>
<code>{extra[9]}</code>
━━━━━━━━━━━━━━━━━━
• Bin Info: 
Pais: {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
Bank: {binreq.json()['bank']} 
Data: {binreq.json()['brand']} - {binreq.json()['level']} - {binreq.json()['type']}
━━━━━━━━━━━━━━━━━━
by: @{callback_query.from_user.username}</b>'''

        # Crear botones
        re_gen = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Regen", callback_data=f"regen:{user_id}")],
        ])

        await callback_query.edit_message_text(texto, reply_markup=re_gen)
        await callback_query.answer("✅ CCs regeneradas exitosamente")
        
    except FloodWait as e:
        await callback_query.answer(
            f"⚠️ Por favor espera {e.value} segundos antes de intentar nuevamente",
            show_alert=True
        )
    except Exception as e:
        print(f"Error en regen callback: {str(e)}")
        await callback_query.answer("❌ Error al regenerar CCs", show_alert=True)

@Client.on_callback_query(filters.regex("regen"))
async def exit(client, message):
    bins = message.message.reply_to_message.text.split('gen ')
    geneo = re.findall(r'[0-9]+',message.message.reply_to_message.text)
    binreq = requests.get(f'https://bins.antipublic.cc/bins/{bins[1][:6]}')
    if 'Invalid BIN' in binreq.text:
        await message.reply('<b>Status Dead ❌ | Invalid BIN.</b>')
        return
    elif 'not found' in binreq.text:
        await message.reply('<b>Status Dead ❌ | not found</b>')
        return
    else:
        # Extraer fechas si existen en la entrada
        fechas = []
        for line in message.message.reply_to_message.text.split('\n'):
            match = re.search(r'<code>\d{6,16}\|(\d{2})\|(\d{2,4})\|\w+</code>', line)
            if match:
                fechas.append((match.group(1), match.group(2)))
        extra = []
        if fechas:
            # Si hay fechas, mantenerlas
            for mes, ano in fechas:
                cc_cvv = Generator(bins[1][:6], 1, True).generate_ccs()[0]
                cc, _, _, cvv = cc_cvv.split('|')
                extra.append(f"{cc}|{mes}|{ano}|{cvv}")
        else:
            # Si no hay fechas, generar tarjetas completas aleatorias
            extra = Generator(bins[1],10,True).generate_ccs()

        cc1 = extra[0]
        cc2 = extra[1]
        cc3 = extra[2]
        cc4 = extra[3]
        cc5 = extra[4]
        cc6 = extra[5]
        cc7 = extra[6]
        cc8 = extra[7]
        cc9 = extra[8]
        cc10 = extra[9]

        texto= f'''<b>Generador ccs

Format: {bins[1]}

<code>{cc1}</code>
<code>{cc2}</code>
<code>{cc3}</code>
<code>{cc4}</code>
<code>{cc5}</code>
<code>{cc6}</code>
<code>{cc7}</code>
<code>{cc8}</code>
<code>{cc9}</code>
<code>{cc10}</code>
━━━━━━━━━━━━━━━━━━
• Bin Info: 
Pais: {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
Bank: {binreq.json()['bank']} 
Data: {binreq.json()['brand']} - {binreq.json()['level']} - {binreq.json()['type']}
━━━━━━━━━━━━━━━━━━
by: @{message.from_user.username}</b>'''
        re_gen = InlineKeyboardMarkup([[InlineKeyboardButton("regen",callback_data=f"regen:{message.from_user.id}")],])

        await message.edit_message_text(texto,reply_markup=re_gen) 