from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from .keyboards import tools_menu

@Client.on_callback_query(filters.regex("^tools:"))
async def tools_callback(client: Client, query: CallbackQuery):
    try:
        user_id = query.from_user.id
        data = query.data.split(":")
        
        if len(data) == 2 and data[1] == str(user_id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
            ])
            
            await query.edit_message_text(
                '''<b>あ » H2 Bot Checker | Tools</b>

【𝙏𝙤𝙤𝙡𝙨 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚】:

↯ » Status    » On ✅
↯ » Cmmd    » $bin
↯ » Format   » $bin 456789
━━
↯ » Status    » On ✅
↯ » Cmmd    » $gen
↯ » Format   » $gen 456789
━━
↯ » Status    » On ✅
↯ » Cmmd    » $rand
↯ » Format   » $rand US
↯ » Format   » /randlist
━━
↯ » Status    » On ✅
↯ » Cmmd    » $extras
↯ » Format   » $extras 456789
━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
—————— <b>あ » H2 Bot Checker</b> ——————</b>''',
                reply_markup=keyboard
            )
            await query.answer("✅ Herramientas disponibles")
        else:
            await query.answer("❌ Solo el usuario que inició el comando puede usar este botón", show_alert=True)
    except MessageNotModified:
        await query.answer("✅ Ya estás en el menú de herramientas", show_alert=False)
    except Exception as e:
        print(f"Error en tools_callback: {str(e)}")
        await query.answer("❌ Error al mostrar las herramientas", show_alert=True) 