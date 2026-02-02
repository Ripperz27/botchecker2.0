from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified

@Client.on_callback_query(filters.regex("^gateways:"))
async def gateways_callback(client: Client, query: CallbackQuery):
    try:
        user_id = query.from_user.id
        data = query.data.split(":")
        
        if len(data) == 2 and data[1] == str(user_id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
            ])
            
            await query.edit_message_text(
                '''<b>あ » H2 Bot Checker | Gateways</b>

【𝙂𝙖𝙩𝙚𝙬𝙖𝙮𝙨 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚】:

━━
↯ » 𝙎𝙩𝙖𝙩𝙪𝙨    » On ✅
↯ » 𝙏𝙮𝙥𝙚    » <i>Braintree Auth</i>
↯ » 𝘾𝙢𝙢𝙙    » $b3
↯ » 𝙁𝙤𝙧𝙢𝙖𝙩   » <code>$b3 cc|mm|yy|cvc</code>
━━
↯ » 𝙎𝙩𝙖𝙩𝙪𝙨    » On ✅
↯ » 𝙏𝙮𝙥𝙚    » <i>Shopify Auth</i>
↯ » 𝘾𝙢𝙢𝙙    » $sh
↯ » 𝙁𝙤𝙧𝙢𝙖𝙩   » <code>$sh cc|mm|yy|cvc</code>
━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
—————— <b>あ » H2 Bot Checker</b> ——————</b>''',
                reply_markup=keyboard
            )
            await query.answer("✅ Gateways disponibles")
        else:
            await query.answer("❌ Solo el usuario que inició el comando puede usar este botón", show_alert=True)
    except MessageNotModified:
        await query.answer("✅ Ya estás en el menú de gateways", show_alert=False)
    except Exception as e:
        print(f"Error en gateways_callback: {str(e)}")
        await query.answer("❌ Error al mostrar los gateways", show_alert=True)

@Client.on_callback_query(filters.regex("^auth:"))
async def auth_callback(client: Client, query: CallbackQuery):
    try:
        user_id = query.from_user.id
        data = query.data.split(":")
        
        if len(data) == 2 and data[1] == str(user_id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Atrás", callback_data=f"gateways:{user_id}")]
            ])
            
            await query.edit_message_text(
                '''<b>あ » H2 Bot Checker | Auth</b>

【𝙂𝙖𝙩𝙚𝙬𝙖𝙮𝙨 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚】:

━━
↯ » 𝙎𝙩𝙖𝙩𝙪𝙨    » On ✅
↯ » 𝙏𝙮𝙥𝙚    » <i>Braintree Auth</i>
↯ » 𝘾𝙢𝙢𝙙    » $b3
↯ » 𝙁𝙤𝙧𝙢𝙖𝙩   » <code>$b3 cc|mm|yy|cvc</code>
━━
↯ » 𝙎𝙩𝙖𝙩𝙪𝙨    » On ✅
↯ » 𝙏𝙮𝙥𝙚    » <i>Shopify Auth</i>
↯ » 𝘾𝙢𝙢𝙙    » $sh
↯ » 𝙁𝙤𝙧𝙢𝙖𝙩   » <code>$sh cc|mm|yy|cvc</code>
━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Active 🟢
—————— <b>あ » H2 Bot Checker</b> ——————</b>''',
                reply_markup=keyboard
            )
            await query.answer("✅ Auth gateways disponibles")
        else:
            await query.answer("❌ Solo el usuario que inició el comando puede usar este botón", show_alert=True)
    except MessageNotModified:
        await query.answer("✅ Ya estás en el menú de Auth", show_alert=False)
    except Exception as e:
        print(f"Error en auth_callback: {str(e)}")
        await query.answer("❌ Error al mostrar los gateways de autenticación", show_alert=True) 