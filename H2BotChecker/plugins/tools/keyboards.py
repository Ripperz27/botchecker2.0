from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Perfil", callback_data=f"profile:{user_id}"),
            InlineKeyboardButton("Gateways", callback_data=f"gateways:{user_id}")
        ],
        [
            InlineKeyboardButton("Herramientas", callback_data=f"tools:{user_id}")
        ]
    ])

def tools_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
    ])

def gateways_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
    ])

def profile_menu(user_id):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Atrás", callback_data=f"back:{user_id}")]
    ]) 