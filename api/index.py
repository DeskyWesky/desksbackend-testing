import requests
import random
from flask import Flask, jsonify, request
import json
import time
import hashlib
import hmac
import base64
from datetime import datetime, timedelta

APP_CREDENTIALS = "OC|34606118765698723|eed22a47cc74b8e387580d7c672eba89"

AppLabCredentials = {
    "Og Gtag": {
        "Credential": APP_CREDENTIALS
    },
    "GameNameHere2": {
        "Credential": "yourcred"
    },
}

class GameInfo:
    def __init__(self):
        self.TitleId = "1DA2C"
        self.SecretKey = "HNH1XX146IRFMI47W5X8N85CO7EYGU5KA5Y7ATW4619COCFDE1"
        self.ApiKey = APP_CREDENTIALS
        self.AppCreds = APP_CREDENTIALS
        self.DiscordWebhookUrl = "https://discord.com/api/webhooks/1479945982799122473/oDmpbmu7geSI83cLDJYPWJU_DwfQmdeHw8nAO3RzXrhNt0rv17nxBcJ0aPx9zpW49ZMf"
        self.ApiKeys = [APP_CREDENTIALS]

    def get_auth_headers(self):
        return {"content-type": "application/json", "X-SecretKey": self.SecretKey}

    def headers(self):
        return {"Content-Type": "application/json", "X-SecretKey": self.SecretKey}

class ApplabInfo:
    def __init__(self):
        self.Credential = None

settings = GameInfo()

Og Gtag = ApplabInfo()
Og Gtag.Credential = AppLabCredentials["Og Gtag"]["Credential"]

GameNamehere2 = ApplabInfo()
GameNamehere2.Credential = AppLabCredentials["GameNameHere2"]["Credential"]

AllApplabs = [Og Gtag, GameNamehere2]

app = Flask(__name__)

used_nonces = {}
used_orgscopes = {}
active_rooms = {}

SUSPICIOUS_PATTERNS = [
    "discord.gg/spm", "discord.gg/", "discord.com/", "dsc.gg/",
    "https://", "http://", "www.", ".gg/", ".com/", "invite/", "server/"
]

EXPECTED_USER_AGENT = "UnityPlayer/2022.3.2f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)"
EXPECTED_UNITY_VERSION = "2022.3.2f1"

def get_client_ip():
    ip = request.headers.get('X-Real-Ip') or request.headers.get('X-Forwarded-For') or request.remote_addr
    if ',' in ip:
        ip = ip.split(',')[0].strip()
    return ip

def check_vpn(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=16974336", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("proxy") or data.get("hosting"):
                send_discord_webhook(
                    "🚫 VPN/Proxy Detected",
                    "",
                    16711680,
                    [
                        {"name": "IP Address", "value": ip_address, "inline": True},
                        {"name": "Proxy", "value": str(data.get("proxy", False)), "inline": True},
                        {"name": "Hosting", "value": str(data.get("hosting", False)), "inline": True},
                        {"name": "Country", "value": data.get("country", "Unknown"), "inline": True},
                        {"name": "ISP", "value": data.get("isp", "Unknown"), "inline": False}
                    ]
                )
                return True
    except Exception as e:
        print(f"VPN check failed: {e}")
    return False

def check_suspicious_nonce(nonce, oculus_id, ip_address, path="Primary"):
    if not nonce:
        return False
    
    nonce_lower = nonce.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in nonce_lower:
            print(f"Blocked suspicious nonce: {nonce}")
            send_discord_webhook(
                "🚫 Malicious Nonce Detected",
                "",
                16711680,
                [
                    {"name": "Nonce", "value": nonce, "inline": False},
                    {"name": "Pattern", "value": pattern, "inline": True},
                    {"name": "Oculus ID", "value": oculus_id or "Unknown", "inline": True},
                    {"name": "IP Address", "value": ip_address, "inline": True},
                    {"name": "Auth Path", "value": path, "inline": True}
                ]
            )
            return True
    return False

def check_if_banned(custom_id):
    try:
        ban_check = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/LoginWithCustomId",
            json={"CustomId": custom_id, "CreateAccount": False},
            headers=settings.headers()
        )
        if ban_check.status_code == 403 and ban_check.json().get("errorCode") == 1002:
            return True, ban_check.json().get("errorDetails", {})
        return False, None
    except:
        return False, None

def cleanup_old_tracking():
    current_time = time.time()
    cutoff_time = current_time - (24 * 3600)
    
    for old_nonce in list(used_nonces.keys()):
        if used_nonces[old_nonce][1] < cutoff_time:
            old_orgscope = used_nonces[old_nonce][0]
            del used_nonces[old_nonce]
            if old_orgscope in used_orgscopes and used_orgscopes[old_orgscope][0] == old_nonce:
                del used_orgscopes[old_orgscope]

def check_ban_evasion(nonce, orgscope, ip_address, path="Primary"):
    cleanup_old_tracking()
    current_time = time.time()
    
    if nonce in used_nonces:
        stored_orgscope, stored_timestamp = used_nonces[nonce]
        if stored_orgscope != orgscope:
            previous_custom_id = f"OCULUS{stored_orgscope}"
            is_previous_banned, ban_details = check_if_banned(previous_custom_id)
            
            if is_previous_banned:
                send_discord_webhook(
                    "🚨 Ban Evasion - Nonce Reuse",
                    "",
                    16711680,
                    [
                        {"name": "Type", "value": "Nonce Reuse from Banned Account", "inline": False},
                        {"name": "Current OrgScope", "value": orgscope, "inline": True},
                        {"name": "Banned OrgScope", "value": stored_orgscope, "inline": True},
                        {"name": "IP", "value": ip_address, "inline": True},
                        {"name": "Time Since Use", "value": f"{int((current_time - stored_timestamp) / 60)} min", "inline": True},
                        {"name": "Path", "value": path, "inline": True}
                    ]
                )
                return True
    
    if orgscope in used_orgscopes:
        stored_nonce, stored_timestamp = used_orgscopes[orgscope]
        if stored_nonce != nonce:
            current_custom_id = f"OCULUS{orgscope}"
            is_current_banned, ban_details = check_if_banned(current_custom_id)
            
            if is_current_banned:
                send_discord_webhook(
                    "🚨 Ban Evasion - Different Nonce",
                    "",
                    16711680,
                    [
                        {"name": "Type", "value": "Banned Account Using Different Nonce", "inline": False},
                        {"name": "OrgScope", "value": orgscope, "inline": True},
                        {"name": "Current Nonce", "value": nonce, "inline": True},
                        {"name": "Previous Nonce", "value": stored_nonce, "inline": True},
                        {"name": "IP", "value": ip_address, "inline": True},
                        {"name": "Path", "value": path, "inline": True}
                    ]
                )
                return True
    
    return False

def store_auth_success(nonce, orgscope):
    current_time = time.time()
    used_nonces[nonce] = (orgscope, current_time)
    used_orgscopes[orgscope] = (nonce, current_time)

def verify_device(playfab_id, platform, ip_address, path="Primary"):
    device_model = "Quest" if platform == "Quest" else "Unknown"
    device_platform = "Android" if platform == "Quest" else "Unknown"
    device_type = "Handheld" if platform == "Quest" else "Unknown"
    
    if device_model == "Quest" and device_platform == "Android" and device_type == "Handheld":
        try:
            requests.post(
                url=f"https://{settings.TitleId}.playfabapi.com/Server/UpdateUserInternalData",
                json={"PlayFabId": playfab_id, "Data": {"Verified": "true"}},
                headers=settings.get_auth_headers()
            )
            send_discord_webhook(
                "✅ Device Verified",
                "",
                65280,
                [
                    {"name": "PlayFab ID", "value": playfab_id, "inline": True},
                    {"name": "Platform", "value": device_platform, "inline": True},
                    {"name": "IP", "value": ip_address, "inline": True},
                    {"name": "Path", "value": path, "inline": True}
                ]
            )
        except Exception as e:
            print(f"Failed to update verification: {e}")
    else:
        try:
            requests.post(
                url=f"https://{settings.TitleId}.playfabapi.com/Admin/BanUsers",
                json={
                    "Bans": [{
                        "PlayFabId": playfab_id,
                        "DurationInHours": 336,
                        "Reason": "Device verification failed"
                    }]
                },
                headers=settings.get_auth_headers()
            )
            send_discord_webhook(
                "🚫 Invalid Device - Banned",
                "",
                16711680,
                [
                    {"name": "PlayFab ID", "value": playfab_id, "inline": True},
                    {"name": "Platform", "value": device_platform, "inline": True},
                    {"name": "IP", "value": ip_address, "inline": True},
                    {"name": "Path", "value": path, "inline": True}
                ]
            )
        except Exception as e:
            print(f"Failed to ban invalid device: {e}")

def verify_custom_id(playfab_id, ip_address, path="Primary"):
    try:
        account_req = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
            json={"PlayFabId": playfab_id},
            headers=settings.get_auth_headers()
        )
        
        if account_req.status_code == 200:
            account_info = account_req.json().get("data", {}).get("UserInfo", {})
            custom_id_info = account_info.get("ServerCustomIdInfo")
            
            if not custom_id_info or not custom_id_info.get("CustomId"):
                ban_and_delete_player(playfab_id, "Missing Custom ID", ip_address, path)
            elif custom_id_info.get("CustomId", "").startswith("OCULUS"):
                custom_id = custom_id_info.get("CustomId")
                org_scope = custom_id[6:]
                
                if len(org_scope) in [16, 17]:
                    send_discord_webhook(
                        "✅ Valid Custom ID",
                        "",
                        65280,
                        [
                            {"name": "PlayFab ID", "value": playfab_id, "inline": True},
                            {"name": "Custom ID", "value": custom_id, "inline": True},
                            {"name": "IP", "value": ip_address, "inline": True},
                            {"name": "Path", "value": path, "inline": True}
                        ]
                    )
                else:
                    ban_and_delete_player(playfab_id, "Invalid org scope length", ip_address, path)
            else:
                ban_and_delete_player(playfab_id, "Invalid Custom ID type", ip_address, path)
    except Exception as e:
        print(f"Auth verification failed: {e}")

def ban_and_delete_player(playfab_id, reason, ip_address, path="Primary"):
    send_discord_webhook(
        "🚫 Auth Failed - Player Removed",
        "",
        16711680,
        [
            {"name": "PlayFab ID", "value": playfab_id, "inline": True},
            {"name": "Reason", "value": reason, "inline": False},
            {"name": "IP", "value": ip_address, "inline": True},
            {"name": "Path", "value": path, "inline": True}
        ]
    )
    
    try:
        requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Admin/BanUsers",
            json={"Bans": [{"PlayFabId": playfab_id, "Reason": reason, "DurationInHours": 672}]},
            headers=settings.get_auth_headers()
        )
        requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Admin/DeletePlayer",
            json={"PlayFabId": playfab_id},
            headers=settings.get_auth_headers()
        )
    except Exception as e:
        print(f"Failed to ban/delete player: {e}")

def send_discord_webhook(title, description, color, fields=None):
    if not settings.DiscordWebhookUrl or "YOUR_WEBHOOK_URL_HERE" in settings.DiscordWebhookUrl:
        return
    
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
    except:
        timestamp = None
    
    field_text = ""
    if fields:
        for field in fields:
            field_text += f"[{field['name']}]: {field['value']}\n"
    
    final_description = f"**Details**\n```ini\n{field_text}```" if field_text else description
    
    embed = {"title": title, "description": final_description, "color": color}
    if timestamp:
        embed["timestamp"] = timestamp
    
    payload = {"embeds": [embed]}
    
    try:
        requests.post(settings.DiscordWebhookUrl, json=payload, timeout=5)
    except Exception as e:
        print(f"Discord webhook failed: {e}")

def validate_orgscoped_id(orgscope):
    try:
        res = requests.get(url=f"https://graph.oculus.com/{orgscope}?access_token={settings.AppCreds}")
        data = res.json()
        return data.get("id") == orgscope
    except:
        return False

def get_meta_alias(oculus_id):
    try:
        alias_req = requests.get(
            f"https://graph.oculus.com/{oculus_id}?access_token={settings.AppCreds}&fields=alias",
            headers={"Content-Type": "application/json"}
        )
        return alias_req.json().get("alias")
    except:
        return None

def validate_nonce(nonce, oculus_id):
    try:
        nonce_check = requests.post(
            url="https://graph.oculus.com/user_nonce_validate",
            json={"access_token": settings.AppCreds, "nonce": nonce, "user_id": oculus_id},
            headers={"Content-Type": "application/json"}
        )
        return nonce_check.status_code == 200 and nonce_check.json().get("is_valid") == True
    except:
        return False

def get_orgscope(oculus_id):
    try:
        org_req = requests.get(
            f"https://graph.oculus.com/{oculus_id}?access_token={settings.AppCreds}&fields=org_scoped_id",
            headers={"Content-Type": "application/json"}
        )
        return org_req.json().get("org_scoped_id")
    except:
        return None

@app.route("/", methods=["POST", "GET"])
def main():
    return """
        <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
            </head>
            <body style="font-family: 'Inter', sans-serif;">
                <h1 style="color: blue; font-size: 30px;">
                    i love desk (discord.gg/luckytag)
                </h1>
            </body>
        </html>
    """

@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    ip_address = get_client_ip()
    
    if check_vpn(ip_address):
        return jsonify({"Message": "VPN or proxy connections are not allowed", "Error": "BadRequest-VPNDetected"}), 403
    
    rjson = request.get_json()
    oculus_id = rjson.get("OculusId")
    nonce = rjson.get("Nonce")
    title = rjson.get("AppId")
    platform = rjson.get("Platform")
    app_ver = rjson.get("AppVersion", "")
    custom_id = rjson.get("CustomId")
    
    if check_suspicious_nonce(nonce, oculus_id, ip_address):
        return jsonify({"Message": "Invalid nonce format detected", "Error": "BadRequest-InvalidNonce"}), 400
    
    if (request.headers.get("User-Agent") != EXPECTED_USER_AGENT or 
        request.headers.get("X-Unity-Version") != EXPECTED_UNITY_VERSION or
        title != settings.TitleId or platform != "Quest" or app_ver != ""):
        return "", 404
    
    if not all([title, nonce, platform, oculus_id]):
        return "", 404
    
    graph_user = None
    for api_key in settings.ApiKeys:
        try:
            response = requests.get(f"https://graph.oculus.com/{oculus_id}?access_token={api_key}&fields=org_scoped_id,alias")
            if response.status_code == 200:
                graph_user = response.json()
                break
        except Exception as e:
            print(f"API key failed: {e}")
            continue
    
    if not graph_user:
        return "", 404
    
    current_orgscope = graph_user.get("org_scoped_id")
    
    if check_ban_evasion(nonce, current_orgscope, ip_address):
        return jsonify({"Message": "Authentication failed", "Error": "BadRequest-InvalidAuth"}), 400
    
    org = custom_id if custom_id else f"OCULUS{current_orgscope}"
    
    login_req = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/LoginWithCustomId",
        json={"CustomId": org, "CreateAccount": True},
        headers=settings.headers()
    )
    
    if login_req.status_code == 200:
        store_auth_success(nonce, current_orgscope)
        
        playfab_id = login_req.json().get("data").get("PlayFabId")
        
        embed = {
            "embeds": [{
                "title": "✅ UserAuthed Correctly",
                "description": f"```ini\n[PlayFab ID]: {playfab_id}\n[IP]: {ip_address}\n[Age]: {rjson.get('AgeCategory', 'N/A')}\n[Username]: {graph_user.get('alias', 'N/A')}```",
                "color": 3447003
            }]
        }
        requests.post("https://discord.com/api/webhooks/1491913655300919326/EpR4YUjIo1lU3c-zpY5Yd8wWw-Dt4f4JtyNKC0WZipN2v0HjZbfNqDjRpJtOM03VOdsU", json=embed)
        
        requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/LinkServerCustomID",
            json={"ServerCustomId": org, "ForceLink": True, "PlayFabId": playfab_id},
            headers=settings.headers()
        )
        
        verify_device(playfab_id, platform, ip_address)
        verify_custom_id(playfab_id, ip_address)
        
        return jsonify({
            "SessionTicket": login_req.json().get("data").get("SessionTicket"),
            "EntityToken": login_req.json().get("data").get("EntityToken").get("EntityToken"),
            "PlayFabId": playfab_id,
            "EntityId": login_req.json().get("data").get("EntityToken").get("Entity").get("Id"),
            "EntityType": login_req.json().get("data").get("EntityToken").get("Entity").get("Type")
        }), 200
    else:
        if login_req.json().get("errorCode") == 1002:
            return jsonify({
                "BanMessage": list(login_req.json().get("errorDetails"))[0],
                "BanExpirationTime": list(login_req.json().get("errorDetails").values())[0][0]
            }), 403
        elif login_req.json().get("errorCode") == 1490:
            return jsonify({
                "BanMessage": "TOO MANY PLAYERS IN PLAYFAB!\nMESSAGE AN OWNER IMMEDIATELY.",
                "BanExpirationTime": "Indefinite"
            }), 403
        return "", 404

@app.route("/api/CachePlayFabId", methods=["POST"])
def cache_playfab_id():
    return jsonify({"Message": "Success"}), 200

@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")
    
    response = requests.post(
        url=f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"}
    )
    
    return jsonify({"result": True}) if response.json().get("success") else jsonify({"error": True})

@app.route("/api/GetAcceptedAgreements", methods=['POST', 'GET'])
def get_accepted_agreements():
    return jsonify({"PrivacyPolicy": "1.1.28", "TOS": "11.05.22.2"}), 200

@app.route("/api/SubmitAcceptedAgreements", methods=['POST', 'GET'])
def submit_accepted_agreements():
    return jsonify({}), 200

@app.route("/api/ConsumeCodeItem", methods=["POST"])
def consume_code_item():
    rjson = request.get_json()
    code = rjson.get("itemGUID")
    playfab_id = rjson.get("playFabID")
    session_ticket = rjson.get("playFabSessionTicket")
    
    if not all([code, playfab_id, session_ticket]):
        return jsonify({"error": "Missing parameters"}), 400
    
    raw_url = "https://github.com/redapplegtag/backendsfrr"
    response = requests.get(raw_url)
    
    if response.status_code != 200:
        return jsonify({"error": "GitHub fetch failed"}), 500
    
    lines = response.text.splitlines()
    codes = {split[0].strip(): split[1].strip() for line in lines if (split := line.split(":")) and len(split) == 2}
    
    if code not in codes:
        return jsonify({"result": "CodeInvalid"}), 404
    
    if codes[code] == "AlreadyRedeemed":
        return jsonify({"result": codes[code]}), 200
    
    grant_response = requests.post(
        f"https://{settings.TitleId}.playfabapi.com/Admin/GrantItemsToUsers",
        json={
            "ItemGrants": [
                {"PlayFabId": playfab_id, "ItemId": item_id, "CatalogVersion": "DLC"}
                for item_id in ["dis da cosmetics", "anotehr cposmetic", "anotehr"]
            ]
        },
        headers=settings.get_auth_headers()
    )
    
    if grant_response.status_code != 200:
        return jsonify({"result": "PlayFabError", "errorMessage": grant_response.json().get("errorMessage", "Grant failed")}), 500
    
    return jsonify({"result": "Success", "itemID": code, "playFabItemName": codes[code]}), 200

@app.route('/api/v2/GetName', methods=['POST', 'GET'])
def get_name():
    return jsonify({"result": f"LUCKY{random.randint(1000, 9999)}"})

def find_available_room(max_players=10):
    for room_id, room_data in active_rooms.items():
        if room_data['player_count'] < max_players:
            return room_id, room_data
    return None, None

def create_new_room():
    room_id = f"GT_{int(time.time())}_{random.randint(1000, 9999)}"
    room_data = {'player_count': 1, 'created_at': time.time(), 'max_players': 10}
    active_rooms[room_id] = room_data
    return room_id, room_data

def join_room(room_id):
    if room_id in active_rooms:
        active_rooms[room_id]['player_count'] += 1
        return active_rooms[room_id]
    return None

def cleanup_old_rooms():
    current_time = time.time()
    rooms_to_remove = [
        room_id for room_id, room_data in active_rooms.items()
        if current_time - room_data['created_at'] > 1800
    ]
    for room_id in rooms_to_remove:
        del active_rooms[room_id]

@app.route("/api/photon", methods=["POST", "GET"])
def photon_auth():
    cleanup_old_rooms()
    
    try:
        getjson = request.get_json() or {}
    except:
        return jsonify({'Error': 'Invalid JSON'}), 400
    
    ticket = getjson.get("Ticket")
    nonce = getjson.get("Nonce")
    platform = getjson.get("Platform")
    user_id = getjson.get("UserId")
    nick_name = getjson.get("username")
    
    user_id = user_id if user_id else (ticket.split('-')[0] if ticket else None)
    
    if not user_id or len(user_id) < 15 or len(user_id) > 17:
        send_discord_webhook(
            "❌ Photon Auth Failed",
            "",
            16711680,
            [
                {"name": "Reason", "value": "Invalid User ID", "inline": False},
                {"name": "User ID", "value": user_id or "None", "inline": True},
                {"name": "Method", "value": request.method, "inline": True}
            ]
        )
        return jsonify({'resultCode': 2, 'message': 'Invalid token', 'userId': None, 'nickname': None})
    
    meta_alias = get_meta_alias(user_id)
    
    if platform != 'Quest':
        send_discord_webhook(
            "❌ Photon Auth Failed",
            "",
            16711680,
            [
                {"name": "Reason", "value": "Invalid Platform", "inline": False},
                {"name": "User ID", "value": user_id, "inline": True},
                {"name": "Platform", "value": platform, "inline": True}
            ]
        )
        return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}), 403
    
    if not nonce:
        send_discord_webhook(
            "❌ Photon Auth Failed",
            "",
            16711680,
            [{"name": "Reason", "value": "Missing Nonce", "inline": False}, {"name": "User ID", "value": user_id, "inline": True}]
        )
        return jsonify({'Error': 'Bad request', 'Message': 'Not Authenticated!'}), 304
    
    req = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
        json={"PlayFabId": user_id},
        headers=settings.get_auth_headers()
    )
    
    if req.status_code == 200:
        user_info = req.json().get("data", {}).get("UserInfo", {})
        nick_name = user_info.get("Username") or meta_alias
        
        room_id, room_data = find_available_room(10)
        if room_id:
            join_room(room_id)
        else:
            room_id, room_data = create_new_room()
        
        response_data = {
            'resultCode': 1,
            'message': f'Authenticated user {user_id.lower()} title {settings.TitleId.lower()}',
            'userId': user_id.upper(),
            'nickname': nick_name,
            'roomId': room_id,
            'playerCount': room_data['player_count'],
            'maxPlayers': room_data['max_players']
        }
        
        try:
            discord_log = {
                "embeds": [{
                    "title": "Photon Authentication",
                    "description": f"```json\n{json.dumps(response_data, indent=2)}```",
                    "color": 65280
                }]
            }
            requests.post(settings.DiscordWebhookUrl, json=discord_log, timeout=5)
        except:
            pass
        
        return jsonify(response_data)
    else:
        send_discord_webhook(
            "❌ Photon Auth Failed",
            "",
            16711680,
            [
                {"name": "Reason", "value": "PlayFab Error", "inline": False},
                {"name": "User ID", "value": user_id, "inline": True},
                {"name": "Status", "value": str(req.status_code), "inline": True}
            ]
        )
        return jsonify({'resultCode': 0, 'message': "Something went wrong", 'userId': None, 'nickname': None})

@app.route("/api/PhotonAuthv2", methods=["POST"])
def photon_auth_v2():
    data = request.get_json(silent=True)
    ip_address = get_client_ip()
    
    if not data:
        send_discord_webhook(
            "Photon Auth v2 Blocked",
            "",
            16711680,
            [{"name": "Reason", "value": "No JSON body", "inline": False}, {"name": "IP", "value": ip_address, "inline": True}]
        )
        return jsonify({"error": "Invalid request"}), 400
    
    player_id = data.get("playerId")
    
    if not player_id:
        send_discord_webhook(
            "🚨 Photon Auth v2 Blocked",
            "",
            16711680,
            [{"name": "Reason", "value": "Missing playerId", "inline": False}, {"name": "IP", "value": ip_address, "inline": True}]
        )
        return jsonify({"error": "playerId is required"}), 403
    
    return jsonify({"success": True, "playerId": player_id}), 200

@app.route('/api/TitleData', methods=['POST', 'GET'])
def titledata():
    response_data = {
        "AutoMuteCheckedHours": {
            "hours": 169
        },
        "AutoName_Adverbs": [
            "Cool", "Fine", "Bald", "Bold", "Half", 
            "Only", "Calm", "Fab", "Ice", "Mad", 
            "Rad", "Big", "New", "Old", "Shy"
        ],
        "AutoName_Nouns": [
            "Gorilla", "Chicken", "Darling", "Sloth", "King", 
            "Queen", "Royal", "Major", "Actor", "Agent", 
            "Elder", "Honey", "Nurse", "Doctor", "Rebel", 
            "Shape", "Ally", "Driver", "Deputy"
        ],
        "BundleBoardSign": "<color=#ff4141>discord.gg/luckytag</color>",
        "BundleKioskButton": "<color=#ff4141>discord.gg/luckytag</color>",
        "BundleKioskSign": "<color=#ff4141>discord.gg/luckytag</color>",
        "BundleLargeSign": "<color=#ff4141>discord.gg/luckytag</color>",
        "EmptyFlashbackText": "discord.gg/luckytag",
        "EnableCustomAuthentication": True,
        "GorillanalyticsChance": 4320,
        "LatestPrivacyPolicyVersion": "2024.09.20",
        "LatestTOSVersion": "2024.09.20",
        "CreditsData": [{"Title": "DEV TEAM", "Entries": ["<color=red>DESK</color>\n<color=red>WHATDOIDO</color><color=red>L1RSON</color>\n"]}],
        "MOTD": "<color=white>WELCOME TO LUCKY TAG!</color>\n<color=cyan>JOIN OUR DISCORD AT DISCORD.GG/LUCKYTAG TO SUPPORT OUR GAME!</color>\n\n<color=yellow>GAME CREATOR: DESK</color>\n<color=orange>OUR CURRENT GAME UPDATE IS WINTER 2024</color>\n\n<color=purple>JOIN OUR DISCORD AND BOOST IT 1X FOR EVERYCOSMETIC (NO STAFF)</color>",
        "SeasonalStoreBoardSign": "<color=#80ff00>RATE THE GAME 5 STARS!</color>\n\n<color=#00ff88>.GG/LUCKYTAG</color>",
        "TOS_2024.09.20": "discord.gg/luckytag",
        "TOBAlreadyOwnCompTxt": "discord.gg/luckytag",
        "TOBAlreadyOwnPurchaseBundle": "discord.gg/luckytag",
        "TOBDefCompTxt": "discord.gg/luckytag",
        "TOBDefPurchaseBtnDefTxt": "discord.gg/luckytag",
        "UseLegacyIAP": False
    }
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9080)
