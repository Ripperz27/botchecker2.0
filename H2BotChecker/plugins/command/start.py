from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Menu Principal", callback_data=f"menu:{user_id}")]
    ])
    
    await message.reply_text(
        f"**👋 ¡Bienvenido {message.from_user.first_name}!**\n\n"
        "Soy un Bot Checker para testeos de CCS.\n"
        "Usa /cmds para ver las opciones disponibles.",
        reply_markup=keyboard
    )