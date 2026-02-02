from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(filters.regex("^profile:"))
async def profile(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data.split(":")
    
    if int(data[1]) != user_id:
        return await callback_query.answer("Botones bloqueados.", show_alert=True)
    
    user = callback_query.from_user
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
    ])
    
    await callback_query.edit_message_text(
        f"""<b>あ » H2 Bot Checker | Perfil</b>

【𝙋𝙚𝙧𝙛𝙞𝙡 𝙄𝙣𝙛𝙤】:

↯ » ID: <code>{user.id}</code>
↯ » Username: @{user.username or "Sin username"}
↯ » Name: <i>{user.first_name}</i> 
↯ » Rango: User

━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
        reply_markup=keyboard
    )