from pyrogram import Client
import asyncio
import os
import sys
from time import perf_counter
import logging
from pyrogram.types import CallbackQuery

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class H2BotChecker():
    def __init__(self):
        self.app = Client(
            name="H2 Bot Checker",
            api_id=,
            api_hash='',
            bot_token='',
            plugins=dict(root="plugins"),
            in_memory=True)

        @self.app.on_callback_query()
        def clod(client, call: CallbackQuery):            
            data = call.data.split(":")
            if call.from_user.id != int(data[1]):
                return call.answer("Botones bloqueados.")
            else: 
                call.continue_propagation()

    def runn(self):
        # Limpiar pantalla de forma multiplataforma
        if os.name == 'nt':  # Windows
            os.system("cls")
        else:  # Linux/Unix/Termux
            os.system("clear")
        logging.basicConfig(level=logging.INFO)
        self.app.run()
        print("Bot corriendo...")

if __name__ == "__main__":
    # from plugins.command.start import start
    # from plugins.command.cmds import start
    # from plugins.command.button.atras import atras
    # from plugins.admin.removeg import bin
    # from plugins.admin.addg import addg
    # from plugins.admin.ban import ban
    # from plugins.admin.unban import unban
    # from plugins.admin.register import register
    # from plugins.command.gateways import gateways
    # from plugins.command.tools import tools
    # from plugins.command.tools2 import tools2
    H2BotChecker().runn()


"""
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌
▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌       ▐░▌▐░▌          ▐░▌       ▐░▌          ▐░▌
▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀█░█▀▀      ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀█░█▀▀ ▐░█▀▀▀▀▀▀▀▀▀ 
▐░▌     ▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌          ▐░▌     ▐░▌  ▐░▌          
▐░▌      ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░▌          ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄▄▄ 
▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
 ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀            ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀                                                                                      
                     𝗥𝗜𝗣𝗣𝗘𝗥𝗭 「🐉」

『✪』User: 1148509764
『✪』Code by: @lxRipperzxl27 👑
"""

#Note: Colocar las proxys aunque por defecto andan desactivadas en session.

