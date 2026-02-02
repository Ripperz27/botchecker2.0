from pyrogram import filters, Client
import requests, re
import sqlite3
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from .luhn_gen import Generator
import random
import os

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
    
    def register_user(self, user_id, username):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (user_id, username) VALUES (?, ?)",
                     (user_id, username))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

@Client.on_message(filters.command('register', prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)
async def register_user(_, message):
    db = Database()
    user_id = message.from_user.id
    username = message.from_user.username or "Sin username"
    
    if db.query_user(user_id):
        await message.reply("Ya estás registrado en el bot.")
        return
    
    if db.register_user(user_id, username):
        await message.reply("✅ Registro exitoso. Ahora puedes usar el bot.")
    else:
        await message.reply("❌ Error al registrarte. Intenta más tarde.")

@Client.on_message(filters.command('gen', prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)  
async def hello(_, message): 
    db = Database()
    querY = db.query_user(int(message.from_user.id))
    
    if querY == None: 
        await message.reply('Usar el comando /register para registrarte.')
        return
    
    if querY['role'] == 'baneado': 
        await message.reply('Usuario baneado')
        return
    
    try:
        ccbin = message.text[len('/gen '):]
        
        if not ccbin: 
            await message.reply("<b>• Gen ccs\n• Format: /gen <code>cards</code>\n• Use: Free</b>", quote=True)
            return
        if len(str(ccbin)) < 6: 
            await message.reply('<b>el bin es menos de 6 digitos | ingrese un bin.</b>')
            return
        geneo = re.findall(r'[0-9]+', message.text)
        if not geneo: 
            await message.reply('<b>Ingrese el bin a generar | error de bin.</b>')
            return

        binreq = requests.get(f'https://bins.antipublic.cc/bins/{ccbin[:6]}')
        
        if binreq.status_code == 520: 
            await message.reply('<i>Invalid BIN.</i>')
            return
        elif 'Invalid BIN' in binreq.text:
            await message.reply('<b>Invalid BIN.</b>')
            return
        elif 'not found' in binreq.text:
            await message.reply('<b>not found</b>')
            return
        
        extra = Generator(ccbin, 10, True).generate_ccs()

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
                
        texto = f'''<b> H2 Checker | Generator CC

Format: {ccbin}

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
        re_gen = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Regen", callback_data=f"regen:{message.from_user.id}")],
        ])
        await message.reply(texto, reply_markup=re_gen, reply_to_message_id=message.id)

    except Exception as e:
        await message.reply(f'<b>• <i>Entrada invalida</i></b>')