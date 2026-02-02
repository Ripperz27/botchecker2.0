from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random
import asyncio
import sqlite3
import os
import requests
import sys
import subprocess

class Database:
    def __init__(self):
        self.db_file = "bot_database.db"
        self.create_tables()
    
    def create_tables(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                     username TEXT,
                     role TEXT DEFAULT 'user',
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()
    
    def query_user(self, user_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        
        if user:
            return {
                'user_id': user[0],
                'username': user[1],
                'role': user[2]
            }
        return None

def get_buttons(user_id):
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔄 Re-Gen", callback_data=f"regen_extras:{user_id}")]
        ]
    )

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

def generate_random_cvv(count: int = 10) -> list:
    return [str(random.randint(100, 999)) for _ in range(count)]

@Client.on_message(filters.command("extras", prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)
async def extras_command(client: Client, m: Message):
    db = Database()
    querY = db.query_user(int(m.from_user.id))
    if querY == None:
        return await m.reply('Usar el comando /register para registrarte.')
    
    if querY['role'] == 'baneado':
        return await m.reply('Usuario baneado')

    text = m.text.split()
    if len(text) < 2:
        return await m.reply(
            f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙏𝙤𝙤𝙡 𝙏𝙮𝙥𝙚】: Extras Generator
【𝙐𝙎𝙀】: <code>$extras xxxxxx</code>
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
            quote=True
        )

    entrada = text[1]
    # Si es una tarjeta completa, extraer el BIN
    if '|' in entrada:
        bin_number = entrada.split('|')[0][:6]
    else:
        bin_number = entrada[:6]
    if not bin_number.isdigit() or len(bin_number) < 6:
        return await m.reply(
            f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙀𝙧𝙧𝙤𝙧】: BIN inválido
【𝙐𝙎𝙀】: <code>$extras xxxxxx</code>
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
            quote=True
        )

    # Obtener información del BIN
    binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_number[:6]}')
    if binreq.status_code == 520 or 'Invalid BIN' in binreq.text or 'not found' in binreq.text:
        return await m.reply('<b>BIN inválido o no encontrado.</b>')

    loading_msg = await m.reply(
        f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙇𝙤𝙖𝙙𝙞𝙣𝙜】: Obteniendo extras...
【𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨】: [□□□□□□□□□□] 0%
—————— <b>あ » H2 Bot Checker </b> ——————</b>""",
        quote=True
    )

    # Simular progreso
    for i in range(1, 11):
        progress = i * 10
        bar = "■" * i + "□" * (10 - i)
        await loading_msg.edit_text(
            f"""<b>あ » H2 Bot Checker | Extras</b>

【𝙇𝙤𝙖𝙙𝙞𝙣𝙜】: Obteniendo extras...
【𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨】: [{bar}] {progress}%
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        )
        await asyncio.sleep(0.2)

    # Generar tarjetas
    cards = generate_random_cc(bin_number[:6])
    dates = generate_random_dates()

    # Construir el mensaje
    message = f"""<b>あ »H2 Bot Checker | Extras</b>

【𝙏𝙤𝙤𝙡 𝙏𝙮𝙥𝙚】: Extras Generator
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
【𝙂𝙚𝙣𝙚𝙧𝙖𝙩𝙚𝙙 𝘽𝙞𝙣𝙨】:
</b>\n"""

    # Agregar las tarjetas generadas
    for i in range(len(cards)):
        message += f"<code>{cards[i]}|{dates[i]}|rnd</code>\n"

    message += f"""<b>あ »H2 Bot Checker | Extras</b>

【𝙄𝙣𝙛𝙤 𝘽𝙞𝙣】:
荣 Bin -» <code>{bin_number[:6]}</code>
荣 Country -» {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
荣 Bank -» {binreq.json()['bank']}
荣 Type -» {binreq.json()['brand']}
荣 Level -» {binreq.json()['level']}
━━━━━━━━━━━━━
【𝙏𝙤𝙩𝙖𝙡】: 10 Extras generadas
【𝙎𝙩𝙖𝙩𝙪𝙨】: Generadas exitosamente ✅
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""

    await loading_msg.edit_text(message, reply_markup=get_buttons(m.from_user.id))

@Client.on_callback_query(filters.regex("^extras_regen:"))
async def extras_regen_callback(client: Client, callback_query):
    try:
        # Obtener el ID del usuario del callback_data
        user_id = int(callback_query.data.split(":")[1])
        
        # Verificar que el usuario que presionó el botón sea el mismo que lo generó
        if callback_query.from_user.id != user_id:
            await callback_query.answer("❌ Solo el usuario que generó las extras puede regenerarlas", show_alert=True)
            return

        db = Database()
        querY = db.query_user(user_id)
        if querY == None:
            await callback_query.answer("❌ Usuario no registrado", show_alert=True)
            return

        # Obtener el BIN del mensaje original
        message_text = callback_query.message.text
        bin_number = None
        
        # Extraer el BIN usando la misma lógica que gen.py
        for line in message_text.split('\n'):
            if "荣 Bin -» " in line:
                bin_number = line.split("荣 Bin -» ")[1].strip()
                if '<' in bin_number:
                    bin_number = bin_number.split('<')[0].strip()
                bin_number = bin_number[:6]
                break

        if not bin_number or len(bin_number) < 6:
            await callback_query.answer("❌ BIN inválido", show_alert=True)
            return

        # Obtener información del BIN
        binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_number}')
        if binreq.status_code == 520 or 'Invalid BIN' in binreq.text or 'not found' in binreq.text:
            await callback_query.answer("❌ BIN inválido o no encontrado", show_alert=True)
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
            [[InlineKeyboardButton("🔄 Re-Gen", callback_data=f"extras_regen:{user_id}")]]
        )

        await callback_query.edit_message_text(message, reply_markup=buttons)
        await callback_query.answer("✅ Extras regeneradas exitosamente")
        
    except Exception as e:
        print(f"Error en extras_regen_callback: {str(e)}")
        await callback_query.answer("❌ Error al regenerar extras", show_alert=True)
