from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import sys
import os
import psutil
import time
from datetime import datetime
import sqlite3
from pyrogram.errors import FloodWait, MessageNotModified

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

@Client.on_message(filters.command("reset", prefixes=["/",".","$","!","%","#"]))
async def reset_bot(client: Client, m: Message):
    try:
        # Mostrar mensaje de carga
        loading_msg = await m.reply(
            f"""<b>あ » H2 Bot Checker | Reset</b>\n\n【𝙇𝙤𝙖𝙙𝙞𝙣𝙜】: Reiniciando bot...\n【𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨】: [□□□□□□□□□□] 0%\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        )

        # Simular progreso
        for i in range(1, 11):
            progress = i * 10
            bar = "■" * i + "□" * (10 - i)
            try:
                await loading_msg.edit_text(
                    f"""<b>あ » H2 Bot Checker | Reset</b>\n\n【𝙇𝙤𝙖𝙙𝙞𝙣𝙜】: Reiniciando bot...\n【𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨】: [{bar}] {progress}%\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
                )
            except MessageNotModified:
                continue
            await asyncio.sleep(0.2)

        # Al final, mostrar solo el mensaje de éxito
        try:
            await loading_msg.edit_text(
                f"""<b>あ » H2 Bot Checker | Reset</b>\n\n【𝙎𝙩𝙖𝙩𝙪𝙨】: Bot reiniciado correctamente ✅\n【𝙈𝙚𝙣𝙨𝙖𝙟𝙚】: El bot se está reiniciando...\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
            )
        except MessageNotModified:
            pass

        # Pequeña pausa para asegurar que el mensaje se muestre
        await asyncio.sleep(1)

        # Reiniciar el bot
        python = sys.executable
        os.execl(python, python, *sys.argv)

    except FloodWait as e:
        await m.reply(
            f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙀𝙧𝙧𝙤𝙧】: FloodWait\n【𝙈𝙚𝙣𝙨𝙖𝙟𝙚】: Por favor espera {e.value} segundos antes de intentar nuevamente\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        )
    except Exception as e:
        print(f"Error en reset_bot: {str(e)}")
        await m.reply(
            f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙀𝙧𝙧𝙤𝙧】: {str(e)}\n【𝙈𝙚𝙣𝙨𝙖𝙟𝙚】: Ocurrió un error al reiniciar el bot\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        ) 