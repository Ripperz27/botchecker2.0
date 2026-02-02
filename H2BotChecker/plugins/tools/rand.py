from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import aiohttp
import json
import os

class Database:
    def __init__(self):
        self.db_file = "bot_database.db"
        self.create_tables()
    
    def create_tables(self):
        import sqlite3
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
        import sqlite3
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

@Client.on_message(filters.command(["rand"], ["/", ".", "$", "!", "%", "#"]))
async def rand(client: Client, m: Message):
    try:
        # Verificar si la tool está habilitada
        if os.path.exists("utils/json/gates.json"):
            with open("utils/json/gates.json", "r") as file:
                gates = json.load(file)
                if not gates.get("rand", True):
                    return await m.reply(
                        "<b>La tool 'rand' está deshabilitada por mantenimiento.</b>",
                        quote=True,
                        parse_mode=ParseMode.HTML
                    )
        
        # Verificar usuario registrado
        db = Database()
        querY = db.query_user(int(m.from_user.id))
        if querY == None:
            return await m.reply('Usar el comando /register para registrarte.')
        if querY['role'] == 'baneado':
            return await m.reply('Usuario baneado')

        # Parsear argumentos
        cmd_parts = m.text.split()
        if len(cmd_parts) < 2:
            return await m.reply(
                "<b>Error, ejemplo: /rand <code>MX - CA - ES - US - FR - UK</code></b>",
                quote=True,
                parse_mode=ParseMode.HTML
            )
        country_code = cmd_parts[1].upper()
        # Validar country code (solo 2 letras)
        if len(country_code) != 2 or not country_code.isalpha():
            return await m.reply(
                f"<b>Código de país inválido '{country_code}'. Ejemplo: /rand US</b>",
                quote=True,
                parse_mode=ParseMode.HTML
            )

        # Obtener datos aleatorios
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://randomuser.me/api/?nat={country_code}&inc=name,location,phone'
            ) as response:
                if response.status != 200:
                    return await m.reply(
                        "<b>Error al obtener datos aleatorios. Intenta más tarde.</b>",
                        quote=True,
                        parse_mode=ParseMode.HTML
                    )
                data = await response.json()

        # Extraer datos
        user_data = data["results"][0]
        address_info = {
            "street": f"{user_data['location']['street']['name']} {user_data['location']['street']['number']}",
            "city": user_data['location']['city'],
            "state": user_data['location']['state'],
            "country": user_data['location']['country'],
            "postcode": user_data['location']['postcode'],
            "phone": user_data['phone']
        }

        # Formatear respuesta
        response_text = f"""
<b>彡 𝙷2 Checker | 𝗚𝗲𝗻 𝗔𝗱𝗱𝗿𝗲𝘀𝘀 𝗙𝗮𝗸𝗲 彡⛔️</b>
━━━━━━━━━━━━━━━━
𝗦𝘁𝗿𝗲𝗲𝘁: <code>{address_info['street']}</code>  
𝗖𝗶𝘁𝘆: <code>{address_info['city']}</code>
𝗦𝘁𝗮𝘁𝗲: <code>{address_info['state']}</code>
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <code>{address_info['country']}</code>
𝗭𝗶𝗽 𝗖𝗼𝗱𝗲: <code>{address_info['postcode']}</code>

𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿: <code>{address_info['phone']}</code>
━━━━━━━━━━━━━━━━
𝗚𝗲𝗻 𝗔𝗱𝗱𝗿𝗲𝘀𝘀 𝗕𝘆: @{m.from_user.username}
━━━━━━━━━━━━━━━━         
"""
        await m.reply(
            response_text,
            quote=True,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except Exception as e:
        await m.reply(
            f"<b>Ocurrió un error: {str(e)}</b>",
            quote=True,
            parse_mode=ParseMode.HTML
        )

@Client.on_message(filters.command(["randlist"], ["/", ".", "$", "!", "%", "#"]))
async def randlist(client: Client, m: Message):
    tabla = (
        "<b>🌎 Lista de países para /rand</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<pre>"
        "País             | Código\n"
        "-----------------|-------\n"
        "Estados Unidos   | US\n"
        "México           | MX\n"
        "Canadá           | CA\n"
        "España           | ES\n"
        "Francia          | FR\n"
        "Reino Unido      | GB\n"
        "Argentina        | AR\n"
        "Brasil           | BR\n"
        "Italia           | IT\n"
        "Alemania         | DE\n"
        "Chile            | CL\n"
        "Colombia         | CO\n"
        "Perú             | PE\n"
        "Venezuela        | VE\n"
        "</pre>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Usa el comando así: /rand US</i>"
    )
    await m.reply(tabla, parse_mode=ParseMode.HTML, quote=True) 