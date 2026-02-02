from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import random
import asyncio
import requests
from .luhn_gen import Generator
from pyrogram.errors import FloodWait

def generate_random_cc(bin_number: str, count: int = 10, exclude_cards: list = None) -> list:
    if exclude_cards is None:
        exclude_cards = []
        
    cards = []
    attempts = 0
    max_attempts = count * 2
    
    while len(cards) < count and attempts < max_attempts:
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        full_number = bin_number + remaining_digits + "xxxx"
        if full_number not in exclude_cards:
            cards.append(full_number)
        attempts += 1
    return cards

def generate_random_dates(count: int = 10) -> list:
    dates = []
    for _ in range(count):
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(24, 29))
        dates.append(f"{month}|{year}")
    return dates

@Client.on_callback_query(filters.regex("^regen_extras:"))
async def extras_regen_callback(client: Client, callback_query: CallbackQuery):
    try:
        # Obtener el ID del usuario del callback_data
        user_id = int(callback_query.data.split(":")[1])
        
        # Verificar que el usuario que presionó el botón sea el mismo que lo generó
        if callback_query.from_user.id != user_id:
            await callback_query.answer("❌ Solo el usuario que generó las extras puede regenerarlas", show_alert=True)
            return

        message_text = callback_query.message.text
        bin_number = None
        
        # Buscar el BIN en el mensaje
        for line in message_text.split('\n'):
            if "荣 Bin -» " in line:
                bin_number = line.split("荣 Bin -» ")[1].strip()
                if '<' in bin_number:
                    bin_number = bin_number.split('<')[0].strip()
                bin_number = bin_number[:6]
                break
        
        if not bin_number:
            await callback_query.answer("❌ Error al obtener el BIN", show_alert=True)
            return

        # Obtener información del BIN
        binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
        if binreq.status_code != 200:
            await callback_query.answer("❌ Error al obtener información del BIN", show_alert=True)
            return

        # Generar tarjetas
        cards = generate_random_cc(bin_number)
        dates = generate_random_dates()

        # Construir el mensaje
        message = f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙏𝙤𝙤𝙡 𝙏𝙮𝙥𝙚】: Extras Generator
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
【𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙞𝙣𝙨】:
</b>\n"""

        # Agregar las tarjetas generadas
        for i in range(len(cards)):
            message += f"<code>{cards[i]}|{dates[i]}|rnd</code>\n"

        message += f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙄𝙣𝙛𝙤 𝘽𝙞𝙣】:
荣 Bin -» <code>{bin_number}</code>
荣 Country -» {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
荣 Bank -» {binreq.json()['bank']}
荣 Type -» {binreq.json()['brand']}
荣 Level -» {binreq.json()['level']}
━━━━━━━━━━━━━
【𝙏𝙤𝙩𝙖𝙡】: 10 Extras generadas
【𝙎𝙩𝙖𝙩𝙪𝙨】: Generadas exitosamente ✅
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔄 Re-Gen", callback_data=f"regen_extras:{user_id}")]]
        )

        await callback_query.edit_message_text(message, reply_markup=buttons)
        await callback_query.answer("✅ Extras regeneradas exitosamente")
        
    except FloodWait as e:
        await callback_query.answer(
            f"⚠️ Por favor espera {e.value} segundos antes de intentar nuevamente",
            show_alert=True
        )
    except Exception as e:
        print(f"Error en extras_regen_callback: {str(e)}")
        await callback_query.answer("❌ Error al regenerar extras", show_alert=True) 