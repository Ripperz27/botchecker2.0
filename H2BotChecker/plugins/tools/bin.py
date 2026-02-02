from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import httpx

@Client.on_message(filters.command("bin", prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)
async def bin_command(client: Client, m: Message):
    text = m.text.split()
    if len(text) < 2:
        return await m.reply(
            f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙐𝙨𝙖𝙜𝙚】: <code>/bin xxxxxx</code>
【𝙀𝙭𝙖𝙢𝙥𝙡𝙚】: <code>/bin 491511</code>
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
            quote=True
        )

    bin_number = text[1][:6]
    if not bin_number.isdigit() or len(bin_number) < 6:
        return await m.reply(
            f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙀𝙧𝙧𝙤𝙧】: BIN inválido
【𝙐𝙎𝙀】: <code>/bin xxxxxx</code>
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
            quote=True
        )

    loading_msg = await m.reply(
        f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙇𝙤𝙖𝙙𝙞𝙣𝙜】: Obteniendo información del BIN...
【𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨】: [□□□□□□□□□□] 0%
—————— <b>あ » H2 Bot Checker</b> ——————</b>""",
        quote=True
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://lookup.binlist.net/{bin_number}')
            if response.status_code == 200:
                bin_data = response.json()
                
                message = f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙄𝙣𝙛𝙤 𝘽𝙞𝙣】:
荣 Bin -» <code>{bin_number}</code>
荣 Type -» {bin_data.get('type', 'Unknown')}
荣 Brand -» {bin_data.get('scheme', 'Unknown')}
荣 Bank -» {bin_data.get('bank', {}).get('name', 'Unknown')}
荣 Country -» {bin_data.get('country', {}).get('name', 'Unknown')} {bin_data.get('country', {}).get('emoji', '')}
荣 Currency -» {bin_data.get('country', {}).get('currency', 'Unknown')}
━━━━━━━━━━━━━
【𝙎𝙩𝙖𝙩𝙪𝙨】: Información obtenida exitosamente ✅
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
                
                await loading_msg.edit_text(message)
            else:
                await loading_msg.edit_text(
                    f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙀𝙧𝙧𝙤𝙧】: No se pudo obtener información del BIN
【𝙎𝙩𝙖𝙩𝙪𝙨】: {response.status_code}
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
                )
    except Exception as e:
        await loading_msg.edit_text(
            f"""<b>あ » H2 Bot Checker | BIN Info</b>

【𝙀𝙧𝙧𝙤𝙧】: {str(e)}
【𝙎𝙩𝙖𝙩𝙪𝙨】: Error al procesar la solicitud
—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        ) 