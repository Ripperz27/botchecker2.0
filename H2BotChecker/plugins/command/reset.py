from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import os
import sys
import sqlite3

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

@Client.on_message(filters.command(["reset"], ["/", ".", "$", "!", "%", "#"]))
async def reset_command(client: Client, m: Message):
    try:
        user_id = m.from_user.id
        db = Database()
        
        if not db.query_user(user_id):
            await m.reply(
                "❌ No estás registrado. Usa /start para registrarte.",
                quote=True,
                parse_mode=ParseMode.HTML
            )
            return
            
        if db.query_user(user_id)['role'] == 'baneado':
            await m.reply(
                "❌ Tu cuenta ha sido baneada. Contacta al administrador.",
                quote=True,
                parse_mode=ParseMode.HTML
            )
            return

        await m.reply(
            '''<b>あ » H2 Bot Checker | Reset</b>

【𝙎𝙩𝙖𝙩𝙪𝙨】: Bot reiniciado correctamente ✅
—————— <b>あ » H2 Bot Checker</b> ——————</b>''',
            quote=True,
            parse_mode=ParseMode.HTML
        )
        
        # Reiniciar el bot
        os.execv(sys.executable, ['python'] + sys.argv)
        
    except Exception as e:
        print(f"Error en reset_command: {str(e)}")
        await m.reply(
            "❌ Ocurrió un error al reiniciar el bot.",
            quote=True,
            parse_mode=ParseMode.HTML
        ) 