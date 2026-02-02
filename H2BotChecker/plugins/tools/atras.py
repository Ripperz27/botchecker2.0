from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from pyrogram.errors import MessageNotModified
from .keyboards import main_menu

@Client.on_callback_query(filters.regex("^back:"))
async def back_callback(client: Client, callback_query: CallbackQuery):
    try:
        user_id = int(callback_query.data.split(":")[1])
        
        if callback_query.from_user.id != user_id:
            await callback_query.answer("❌ Solo el usuario que inició el comando puede usar este botón", show_alert=True)
            return

        await callback_query.edit_message_text(
            f"""<a href="https://t.me/H2BotChecker">↯</a> » 𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤 a H2 Bot Checker  

𝘌𝘴 𝘶𝘯 𝘱𝘭𝘢𝘤𝘦𝘳 𝘮𝘳 @{callback_query.from_user.username}, 𝘱𝘶𝘦𝘥𝘦𝘴 𝘮𝘢𝘯𝘦𝘫𝘢𝘳 𝘺 𝘤𝘰𝘯𝘰𝘤𝘦𝘳 𝘯𝘶𝘦𝘴𝘵𝘳𝘢 𝘭𝘪𝘴𝘵𝘢 𝘥𝘦 𝘎𝘢𝘵𝘦𝘸𝘢𝙮𝙨, 𝘛𝘰𝘰𝘭𝘴, 𝘊𝘰𝘮𝘮𝘖𝘯𝘥𝘴, 𝘦𝘯 𝘦𝘭 𝘢𝘱𝘢𝘳𝘵𝘢𝘥𝘰 𝘥𝘦 𝘣𝘰𝘵𝘰𝘯𝘦𝘴.
<a href="https://t.me/H2BotChecker">»</a><i> Mas información</i> -» <a href="https://t.me/H2BotChecker">𝘾𝙖𝙣𝙖𝙡 Of ✨</a>""",
            reply_markup=main_menu(user_id)
        )
        await callback_query.answer("✅ Menú principal")
        
    except MessageNotModified:
        await callback_query.answer("✅ Ya estás en el menú principal", show_alert=False)
    except Exception as e:
        print(f"Error en back_callback: {str(e)}")
        await callback_query.answer("✅ Menú principal", show_alert=False) 