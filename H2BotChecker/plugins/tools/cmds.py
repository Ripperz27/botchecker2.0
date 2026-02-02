from pyrogram import Client, filters
from .keyboards import main_menu

@Client.on_message(filters.command('cmds', prefixes=["/",".","$","!","%","#"]))
async def start(client, m):
    await client.send_photo(
        chat_id=m.chat.id,
        photo='https://i.imgur.com/wWb23N0.jpeg',
        caption=f"""<a href="https://t.me/H2BotChecker">↯</a> » 𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤 a H2 Bot Checker  

𝘌𝘴 𝘶𝘯 𝘱𝘭𝘢𝘤𝘦𝘳 𝘮𝘳 @{m.from_user.username}, 𝘱𝘶𝘦𝘥𝘦𝘴 𝘮𝘢𝘯𝘦𝘫𝘢𝘳 𝘺 𝘤𝘰𝘯𝘰𝘤𝘦𝘳 𝘯𝘶𝘦𝘴𝘵𝘳𝘢 𝘭𝘪𝘴𝘵𝘢 𝘥𝘦 𝘎𝘢𝘵𝘦𝘸𝘢𝙮𝙨, 𝘛𝘰𝘰𝘭𝘴, 𝘊𝘰𝘮𝘮𝘖𝘯𝘥𝘴, 𝘦𝘯 𝘦𝘭 𝘢𝘱𝘢𝘳𝘵𝘢𝘥𝘰 𝘥𝘦 𝘣𝘰𝘵𝘰𝘯𝘦𝘴.
<a href="https://t.me/H2BotChecker">»</a><i> Mas información</i> -» <a href="https://t.me/H2BotChecker">𝘾𝙖𝙣𝙖𝙡 Of ✨</a>""",
        reply_markup=main_menu(m.from_user.id)
    ) 