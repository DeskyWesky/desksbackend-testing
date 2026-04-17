import requests
from flask import Flask, request, jsonify, abort
import json
import base64
import string
import uuid
import jwt
from pymongo import MongoClient
import random



class PlayFabInfo():
    def __init__(playfab):
        playfab.TitleId : str = None
        playfab.SecretKey : str = None

class AppInfo():
    def __init__(app):
        app.Credential : str = None

PfInfo = PlayFabInfo()
PfInfo.TitleId = "1DA2C"
PfInfo.SecretKey = "HNH1XX146IRFMI47W5X8N85CO7EYGU5KA5Y7ATW4619COCFDE1"

Og Gtag = AppInfo()
Og Gtag.Credential = "OC|34606118765698723|eed22a47cc74b8e387580d7c672eba89"

app = Flask(__name__)

Headers = {
    "X-SecretKey": PfInfo.SecretKey,
    "Content-Type": "application/json"
}

DefaultHeaders = {
    "Content-Type": "application/json"
}

TuffDb = MongoClient("mongodb+srv://micheal:cat@ogtag.bgipd8l.mongodb.net/")
db = TuffDb["Db"]
players = db["Players"]

zz = MongoClient("mongodb+srv://micheal:cat@ogtag.bgipd8l.mongodb.net/")
zzzczx = zz["Db"]
Banned = zzzczx["BlockedHwids"]



def BannedLogings(t: str, d: str):
    requests.post(
        url=f"https://discord.com/api/webhooks/1494839878758961252/46jyieoeCTFTdDAxNydHcUAA1uZgMrwutiz7dzq2HoDfOCcuhjsP8ZvUxI7vS4xR9YaM",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": t,
                    "description": d,
                    "color": 0x8B0000
                }
            ],
            "attachments": []
        }
    )
    return
def AddToDb(Id: str, Token: str, UserId: str, Hwid: str):
    p = players.find_one({
        "UserId": UserId
    })
    if p:
        return p["MothershipId"]
    players.insert_one({
        "MothershipId": Id,
        "Token": Token,
        "UserId": UserId,
        "Hwid": Hwid
    })
    return Id
def GenToken():
    lenght = random.randint(22, 40)
    digits = string.ascii_letters + string.digits
    randmshit = ''.join(random.choice(digits) for _ in range(lenght))

    return randmshit
def b64Decode(Val: str):
    b = base64.b64decode(Val)
    r = b.decode(encoding="utf-8")
    return r
def CheckIfbanned(hwid: str):
    e = Banned.find_one({
        "Hwid": hwid
    })
    if e:
        return True
    else:
        return False
def CheckMothershipToken(Token: str):
    r = players.find_one({
        "Token": Token
    })
    if r:
        return True
    else:
        return False

def SuccessComplete(r: str, d: str, Id: str):
    r = players.find_one({
        "MothershipId": Id
    })
    if r:
        return 
    requests.post(
        url="https://discord.com/api/webhooks/1494840084317601832/mZq90pCWaSZgZx7LtpKzo30AlMWnzKc81F-eIOJjv6yzzw5Qi5-2hDSqFnX3vjltd7QC",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": r,
                    "color": 0x57f287,
                    "description": d
                }
            ],
            "attachments": []
        }
    )    
    return
def SuccessBegin(t: str, d: str):
    requests.post(
        url="https://discord.com/api/webhooks/1479945982799122473/oDmpbmu7geSI83cLDJYPWJU_DwfQmdeHw8nAO3RzXrhNt0rv17nxBcJ0aPx9zpW49ZMf",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": t,
                    "description": d,
                    "color": 0x57f287
                }
            ],
            "attachments": []
        }
    )    
    return

def CheckMothershipId(Id: str):
    r = players.find_one({
        "MothershipId": Id
    })
    if r:
        return True
    else:
        return False
    
def GenerateChallangeNonce():
    lenght = random.randint(22, 172)
    digits = string.ascii_letters + string.digits
    randmshit = ''.join(random.choice(digits) for _ in range(lenght))
    

    encoded = base64.b64encode(randmshit.encode('utf-8')).decode('utf-8')
    challangenonce = encoded.replace('+', '-').replace('/', '_')
    return challangenonce

def FailedMothership(t: str, d: str):
    r = requests.post(
        url="https://discord.com/api/webhooks/1494840291981525102/UJU0lUVFl-Iv7vxFZ72zrusLA6OCYLy0JO3aQPfwArGeUmi-T9vOd282cn6GMNxzKYH-",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": t,
                    "description": d,
                    "color": 0x8B0000
                }
            ],
            "attachments": []
        }
    )
    return
def BanUser(PlayerId: str, Duration: str, Reason: str):
    requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/BanUsers",
        headers=Headers,
        json={
            "Bans": [
                {
                    "PlayFabId": PlayerId,
                    "DurationInHours": Duration,
                    "Reason": Reason
                }
            ]
        }
    )
    print("Success")

        
def BadNonce(payload):
        url = "https://discord.com/api/webhooks/1494840394729525358/0SCJC-pFoObn7GW9gdMlQ-cfHUE5V1lpsib0jEp0IoJcTSmDKU_L9IsX_Z-gCGnoztDB"
        headers = {"Content-Type": "application/json"}
        requests.post(url=url, json=payload, headers=headers)

def SusSPM(payload):
        url = "https://discord.com/api/webhooks/1426984555927306291/5D50a2uOS4RUHyhTaTP_NBMhoi8ddQSOIz8JPyktoDrCP2pDZcLOfmFLkEyh3LBV75NC"
        headers = {"Content-Type": "application/json"}
        requests.post(url=url, json=payload, headers=headers)

def PassedSpm(payload):
        url = "https://discord.com/api/webhooks/1437596145122807929/ezEjKGGq0Dljfv0w8PsKyOa5TVr417hw-aYTzN79OzO_aA-raUC8Vji6R_6ou4H8-DLX"
        headers = {"Content-Type": "application/json"}
        requests.post(url=url, json=payload, headers=headers)


def banPlayer(userid, reason, hours):
        url = "https://42638.playfabapi.com/Server/BanUsers"
        headers = {
            "X-SecretKey": "1FG8HPC81TSOK4CPFCI1ZONT4UQBPOQD8WQP69JUE98GNHASZO",
            "content-type": "application/json"}
        payload = {
             "Bans": [
                  {
                       "PlayFabId": userid,
                       "Reason": reason,
                       "DurationInHours": hours
                }
             ]
        }
        requests.post(url=url, json=payload, headers=headers)

def DeleteUser(PlayerId: str):
    requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/BanUsers",
        headers=Headers,
        json={
            "PlayFabId": PlayerId
        }
    )
    print("Success")

def GrantItem(PlayerId: str, ItemId: str):
    requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/GrantItemsToUser",
        headers=Headers,
        json={
            "PlayFabId": PlayerId,
            "ItemIds": [
                ItemId
            ],
            "CatalogVersion": "DLC"
        }
    )
def GrantShinyRocks(PlayfabId: str, Ammount: str):
    requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Admin/AddUserVirtualCurrency",
        headers=Headers,
        json={
            "PlayFabId": PlayfabId,
            "Amount": Ammount,
            "VirtualCurrency": "SR"
        }
    )

def CheckPlayFabId(PlayFabId: str):
    r = requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Admin/GetUserAccountInfo",
        headers=Headers,
        json={
            "PlayFabId": PlayFabId
        }
    )
    
    if r.status_code == 200:
        rjson = r.json()
        return rjson
    else:
        return False
    
def CheckSessionTicket(SessionTicket: str):
    r = requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/AuthenticateSessionTicket",
        headers=Headers,
        json={
            "SessionTicket": SessionTicket
        }
    )
    if r.status_code == 200:
        return True
    else:
        return False
def CheckOrgscope(orgscope: str):
    r = requests.get(
        url=f"https://graph.oculus.com/{orgscope}?access_token={Og Gtag.Credential}&fields=org_scoped_id,alias"
    )
    if r.status_code == 200:
        rjson = r.json()
        return rjson
    else:
        return False

def CheckNonce(nonce: str, userid: str):
    r = requests.post(
        url=f"https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={userid}&access_token={Og Gtag.Credential}",
        headers=DefaultHeaders
    )
    rjson = r.json()
    if rjson.get("is_valid") == True:
        return True
    else:
        return False

def PfAuthFailed(t: str, d: str):
    r = requests.post(
        url="https://discord.com/api/webhooks/1479943617312461033/o8MYAlYWG0lFcn-hfrY91VKimAV0xBpUBx_WK_82pRxanltcbfnvnbwgP3r-N0Mhrq1o",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": t,
                    "description": d,
                    "color": 0x8B0000
                }
            ],
            "attachments": []
        }
    )
    if r.status_code == 204:
        return True
    else:
        return False
    

def VpnUserBan(t: str, d: str):
    r = requests.post(
        url="https://discord.com/api/webhooks/1494840909999640666/8vDKaDT6wcEMwNHA8SbSrNBN011U-OBJyXKtVOujMPkbycgTE59_lW0y_HBvMCF97ctu",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": t,
                    "description": d,
                    "color": 0x8B0000
                }
            ],
            "attachments": []
        }
    )
    if r.status_code == 204:
        return True
    else:
        return False
def AntiVpn(ip: str):
    r = requests.get(
        url=f"http://ip-api.com/json/{ip}?fields=16974336"
    )
    rjson = r.json()
    if rjson.get("proxy") == True or rjson.get("hosting") == True:
        return False
    else:
        return True

def CheckAttestation(Token: str):
    r = requests.get(
        url=f"https://graph.oculus.com/platform_integrity/verify?token={Token}&access_token={Og Gtag.Credential}"
    )
    rjson = r.json().get("data", {})[0]
    if rjson.get("message") == "success":
        return rjson
    else:
        return False
def PfAuthSuccess(Orgscope: str, OculusId: str, PlayFabId: str, EntityToken: str, SessionTicket: str, Platform: str):
    requests.post(
        url="https://discord.com/api/webhooks/1479943053950062803/6WZO7ft4wpRBCrD1rL-CP4VeA86pJvCttcXSToQLbuZEw-tLJDQZwY2NsbeiGVGlZqFK",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": "Success Auth",
                    "color": 0x1f8b4c,
                    "fields": [
                        {
                            "name": "OrgScopedID",
                            "value": f"```{Orgscope}```",
                            "inline": True
                        },
                        {
                            "name": "OculusId",
                            "value": f"```{OculusId}```",
                            "inline": True
                        },
                        {
                            "name": "PlayFabId",
                            "value": f"```{PlayFabId}```",
                            "inline": False
                        },
                        {
                            "name": "EntityToken",
                            "value": f"```{EntityToken}```",
                            "inline": True
                        },
                        {
                            "name": "SessionTicket",
                            "value": f"```{SessionTicket}```"
                        },
                        {
                            "name": "Platform",
                            "value": f"```{Platform}```"
                        }
                    ]
                }
            ]
        }
    )
    return

def PfAuthSuccessNewUpd(Orgscope: str, OculusId: str, PlayFabId: str, EntityToken: str, SessionTicket: str, Platform: str, MothershipId: str, MothershipToken: str, AccountCreationTime: str):
    requests.post(
        url="https://discord.com/api/webhooks/1479943053950062803/6WZO7ft4wpRBCrD1rL-CP4VeA86pJvCttcXSToQLbuZEw-tLJDQZwY2NsbeiGVGlZqFK",
        headers=DefaultHeaders,
        json={
            "embeds": [
                {
                    "title": "Success Auth",
                    "color": 0x1f8b4c,
                    "fields": [
                        {
                            "name": "OrgScopedID",
                            "value": f"```{Orgscope}```",
                            "inline": True
                        },
                        {
                            "name": "OculusId",
                            "value": f"```{OculusId}```",
                            "inline": True
                        },
                        {
                            "name": "PlayFabId",
                            "value": f"```{PlayFabId}```",
                            "inline": False
                        },
                        {
                            "name": "AccountCreation",
                            "value": f"```{AccountCreationTime}```",
                            "inline": True
                        },
                        {
                            "name": "EntityToken",
                            "value": f"```{EntityToken}```",
                            "inline": True
                        },
                        {
                            "name": "SessionTicket",
                            "value": f"```{SessionTicket}```"
                        },
                        {
                            "name": "Platform",
                            "value": f"```{Platform}```"
                        },
                        {
                            "name": "MothershipID",
                            "value": f"```{MothershipId}```",
                            "inline": True
                        },
                        {
                            "name": "MothershipToken",
                            "value": f"```{MothershipToken}```",
                            "inline": True
                        }
                    ]
                }
            ]
        }
    )
    return


@app.route('/api/SaveAgreements', methods=['POST'])
def save_legal_agreements():
    data = request.json
    
    return jsonify({"PrivacyPolicy": "2024.03.07", "TOS": "11.05.22.2"})


@app.route('/api/LoadAgreements', methods=['POST'])
def load_legal_agreements():
    data = request.json

    return jsonify({"PrivacyPolicy": "2024.03.07", "TOS": "11.05.22.2"})


@app.route("/api/CheckForBadName", methods=["POST"])
def Check():
    r = request.get_json()
    a = r.get("FunctionArgument", {})
    room = a.get("forRoom")
    name = a.get("name")
    PfId = r.get("CallerEntityProfile").get("Lineage").get("NamespaceId")
    test = r.get("pl")

    BadNames = [
    "NAZI", "ADOLFHITLER", "NAZ1", "FAG", "FAGGOT", "NIGGER", "NIGGA",
    "NIG", "SLAVE", "SLAVEOWNER", "PORN", "PORNOWNER", "PORNHUB",
    "XVIDEOS", "XVIDEOSOWNER","H1TLER", "HITLER", "KKK", "PUSSY", 
    "CUNT", "TTTPIG", "K9", "XXX", "CHILDPORN", "TEST", "NIGGERFAGGOT"  # add more if you want
]
    if name in BadNames:
        BanUser(PfId, 2, f"Bad Name {name}")
        return jsonify({
            "result": 2
        })
    else:
        return jsonify({
            "result": 0
        })




@app.route("/api/GetRandomName", methods=["POST"])
def GetRandomName():
    name = random.randint(1111, 5000)
    return jsonify({
        "Name": f"SPEEDY{name}"
    })
@app.route("/api/ReturnCurrentVersionV2", methods=["POST"])
def ReturnCurrentVersionV2():
    r = request.get_json()
    CurrentVersion = r.get("CurrentVersion")
    UpdatedSynchTest = r.get("UpdatedSynchTest")
    print(CurrentVersion)
    if CurrentVersion != "yourgameversion":
        return jsonify({
        "SynchTime": UpdatedSynchTest,
        "Fail": True,
        "ResultCode": 1,
        "BannedUsers": 67
    }), 400

    return jsonify({
        "SynchTime": UpdatedSynchTest,
        "Fail": False,
        "ResultCode": 0,
        "BannedUsers": 67
    }), 200


@app.route("/titledata", methods=["POST"])
def Tdata():
    return jsonify({
  "EnableCustomAuthentication": "true",
  "MOTD": "<color=magenta>WELCOME TO OG TAG METRO 2024!\n<color=cyan>JOIN THE DISCORD: DISCORD.GG/OG-TAG</color>\n<color=lime>CREDITS: SYSTEM, FROSTY, TASDIAM, RAIDER, MICHEAL, COLLS & SCREAMINGCAT </color>\n<color=white>ADMIN BADGE IS FOR OWNERS!\n</color></color><color=red>BOOST DISCORD.GG/OG-TAG FOR EVERY COSMETIC!</color>\n<color=yellow>IF YOU LOST COSMETICS JOIN THE DISCORD</color>",
  "PrivacyPolicy_2024.03.07": "JOIN THE DISCORD SERVER: DISCORD.GG/OG-TAG",
  "LatestPrivacyPolicyVersion": "2024.03.07",
  "LatestTOSVersion": "11.05.22.2",
  "BundleBoardSign": "<color=yellow>BUY THIS TO GET EVERY COSMETIC & UNRELEASED SWEATER</color>",
  "BundleKioskSign": "<color=yellow>$10</color>",
  "BundleLargeSign": "<color=red>$10</color>",
  "SeasonalStoreBoardSign": "<color=orange>METRO 2024!</color>",
  "BundleKioskButton": "<color=yellow>$10</color>",
  "UseLegacyIAP": "false",
  "AutoMuteCheckedHours": "336",
  "AutoName_Adverbs": "[\"Cool\",\"Fine\",\"Bald\",\"Bold\",\"Half\",\"Only\",\"Calm\",\"Fab\",\"Ice\",\"Mad\",\"Rad\",\"Big\",\"New\",\"Old\",\"Shy\"]",
  "AutoName_Nouns": "[\"Gorilla\",\"Chicken\",\"Darling\",\"Sloth\",\"King\",\"Queen\",\"Royal\",\"Major\",\"Actor\",\"Agent\",\"Elder\",\"Honey\",\"Nurse\",\"Doctor\",\"Rebel\",\"Shape\",\"Ally\",\"Driver\",\"Deputy\"]",
  "EmptyFlashbackText": "\"FLOOR TWO NOW OPEN\\n FOR BUSINESS\\n\\nSTILL SEARCHING FOR\\nBOX LABELED 2021\"",
  "GorillanalyticsChance": "4320",
  "CreditsData": "[{\"Title\":\"DEV TEAM\",\"Entries\":[\"Lucky \\\"NtsFranz\\\" Franzluebbers\",\"Carlo Grossi Jr\",\"Cody O'Quinn\",\"Craig Abell\",\"David Neubelt\",\"David Yee\",\"Derek \\\"DunkTrain\\\" Arabian\",\"Duncan \\\"rev2600\\\" Carroll\",\"Elie Arabian\",\"Eric “8on2” Kearns\",\"John Sleeper\",\"Johnny Wing\",\"Jonathan \\\"Jonny D\\\" Dearborn\",\"Jonathan \\\"JHameltime\\\" Hamel\",\"Jordan \\\"CircuitLord\\\" J.\",\"Haunted Army\",\"Kaleb \\\"BiffBish\\\" Skillern\",\"Kerestell Smith\",\"Keith \\\"ElectronicWall\\\" Taylor\",\"Mark Putong\",\"Matt \\\"Crimity\\\" Ostgard\",\"Nick Taylor\",\"Riley O'Callaghan\",\"Ross Furmidge\",\"Zac Mroz\"]},{\"Title\":\"SPECIAL THANKS\",\"Entries\":[\"Alpha Squad\",\"Caroline Arabian\",\"Clarissa & Declan\",\"Calum Haigh\",\"EZ ICE\",\"Gwen\",\"Laura \\\"Poppy\\\" Lorian\",\"Lilly Tothill\",\"Meta\",\"Mighty PR\",\"Sasha \\\"Kayze\\\" Sanders\",\"Scout House\",\"The \\\"Sticks\\\"\"]},{\"Title\":\"MUSIC BY\",\"Entries\":[\"Stunshine\",\"David Anderson Kirk\",\"Jaguar Jen\",\"Audiopfeil\",\"Owlobe\"]}]",
  "bannedusers": "17",
  "bundleData": "{\"Items\":[{\"isActive\":false,\"skuName\":\"2023_march_pot_o_gold\",\"shinyRocks\":\"5000\",\"playFabItemName\":\"LSAAU.\",\"majorVersion\":1,\"minorVersion\":1,\"minorVersion2\":39},{\"skuName\":\"2023_sweet_heart_bundle\",\"playFabItemName\":\"LSAAS.\",\"shinyRocks\":0,\"isActive\":true},{\"skuName\":\"2022_launch_bundle\",\"playFabItemName\":\"LSAAP2.\",\"shinyRocks\":10000,\"isActive\":false},{\"skuName\":\"early_access_supporter_pack\",\"playFabItemName\":\"Early Access Supporter Pack\",\"shinyRocks\":0,\"isActive\":false}]}",
  "BuilderTable01": "",
  "BuilderTableConfiguration": "{\"version\":0,\"TableResourceLimits\":[10000,2500,200],\"PlotResourceLimits\":[1500,375,30],\"DroppedPieceLimit\":100}",
  "BundleBoardSign_1.1.46": "x",
  "MuteThresholds": "\"[{\\\"name\\\":\\\"low\\\",\\\"threshold\\\":30},{\\\"name\\\":\\\"high\\\",\\\"threshold\\\":50}]\"",
  "PrivacyPolicy_1.1.28": "DISCORD.GG/OG-TAG”\"",
  "Versions": "{\"CreditsData\":11,\"MOTD_1.1.38\":8,\"MOTD_1.1.39\":7,\"bundleData\":1,\"BundleLargeSign_1.1.40\":1,\"BundleBoardSign_1.1.40\":0,\"BundleKioskSign_1.1.40\":1,\"BundleKioskButton_1.1.40\":0,\"SeasonalStoreBoardSign_1.1.40\":0,\"MOTD_1.1.40\":0,\"MOTD_1.1.42\":2,\"MOTD_1.1.43\":0,\"SeasonalStoreBoardSign_1.1.43\":0,\"MOTD_1.1.45\":10,\"MOTD_1.1.46\":1}",
  "VotekickDuration": "10",
    "DeployFeatureFlags": {
        "flags": [
            {
                "name": "2024-05-ReturnCurrentVersionV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-05-ReturnMyOculusHashV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-05-TryDistributeCurrencyV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-05-AddOrRemoveDLCOwnershipV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-05-BroadcastMyRoomV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-06-CosmeticsAuthenticationV2",
                "value": 0,
                "valueType": "percent"
            },
            {
                "name": "2024-08-KIDIntegrationV1",
                "value": 0,
                "valueType": "percent",
                "alwaysOnForUsers": [
                    ""
                ]
            }
            ]
        },
    })


@app.route("/api/CachePlayFabId", methods=["POST"])
def cache():
    r = request.get_json()
    Platform = r.get("Platform")
    SessionTicket = r.get("SessionTicket")
    PlayFabId = r.get("PlayFabId")
    if not CheckSessionTicket(sessionticket=SessionTicket):
        return "",401
    if Platform != "Quest":
        return "",401
    if not CheckPlayFabId(Playfabid=PlayFabId):
        return "",401
    
    return jsonify({
        "message": "Success",
        "PlayFabId": PlayFabId
    })


@app.route("/api/PlayFabAuthentication", methods=["POST"])
def PfAuth():
    r = request.get_json()
    CustomId = r.get("CustomId", "Missing")
    OculusId = r.get("OculusId", "Missing")
    Platform = r.get("Platform", "Missing")
    Nonce = r.get("Nonce", "Missing")
    AppVersion = r.get("AppVersion", "Missing")
    Orgscope = CustomId.replace("OCULUS", "")
    Ip = request.headers.get("X-Real-Ip", "Missing")
    UserAgent = request.headers.get("User-Agent", "Missing")
    Unityversion = request.headers.get("X-Unity-Version", "Missing")
    Accept = request.headers.get("Accept-Encoding", "Missing")

    if Accept != "deflate, gzip":
        PfAuthFailed(f"Incorrect Accept-Encoding {Accept}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if UserAgent != "UnityPlayer/2022.3.2f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)":
        PfAuthFailed(f"Incorrect UserAgent {UserAgent}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if Unityversion != "2022.3.2f1":
        PfAuthFailed(f"Incorrect UnityVersion {Unityversion}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403 

    if Platform != "Quest":
        PfAuthFailed(f"Incorrect Platform {Platform}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not CheckOrgscope(Orgscope):
        PfAuthFailed(f"Invalid OrgScopedID {Orgscope}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not CheckNonce(nonce=Nonce, userid=OculusId):
        PfAuthFailed(f"Invalid Nonce", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not AntiVpn(Ip):
        VpnUserBan("Vpn User Caught LOL", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "Turn Off Your Vpn | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    
    UserInfo = CheckOrgscope(Orgscope)
    metaUser = UserInfo["alias"]
    
    pfreq = requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/LoginWithServerCustomId",
        headers=Headers,
        json={
            "ServerCustomId": CustomId,
            "CreateAccount": True
        },
        timeout=10
    )
    if pfreq.status_code == 200:
        data = pfreq.json().get("data", {})
        SessionTicket = data.get("SessionTicket", 'Missing')
        PlayFabId = data.get("PlayFabId", 'Missing')
        EntityToken = data.get("EntityToken", {}).get("EntityToken","Missing")
        EntityId = data.get("EntityToken", {}).get("Entity", {}).get("Id")
        EntityType = data.get("EntityToken", {}).get("Entity", {}).get("Type")

        PfAuthSuccess(    
            Orgscope=Orgscope,
            OculusId=OculusId,
            PlayFabId=PlayFabId,
            EntityToken=EntityToken,
            SessionTicket=SessionTicket,
            Platform=Platform
        )
        return jsonify({
            "PlayFabId": PlayFabId,
            "SessionTicket": SessionTicket,
            "EntityId": EntityId,
            "EntityType": EntityType,
            "EntityToken": EntityToken
        }), 200
    else:
        if pfreq.status_code == 403:
            da = pfreq.json()
            if da.get("errorCode") == 1002:
                Details = da.get("errorDetails", {})
                Reason = next(iter(Details))
                Expiration = next(iter(Details[Reason]))
                return jsonify({
                'BanMessage': Reason,
                'BanExpirationTime': Expiration
            }), 403
            else:
                if pfreq.status_code == 429:
                    PfAuthFailed("Too Many Requests To Join", d=None)
                    return "",404
                


@app.route("/api/PlayFabAuthentication/NewerUpdates", methods=["POST"])
def PfAuthNew():
    r = request.get_json()
    OculusId = r.get("OculusId", "Missing")
    Platform = r.get("Platform", "Missing")
    Nonce = r.get("Nonce", "Missing")
    MothershipId = r.get("MothershipId", "Missing")
    MothershipToken = r.get("MothershipToken", "Missing")
    MotheshipEnvId = r.get("MotheshipEnvId", "Missing")
    Ip = request.headers.get("X-Real-Ip", "Missing")
    UserAgent = request.headers.get("User-Agent", "Missing")
    Unityversion = request.headers.get("X-Unity-Version", "Missing")
    Accept = request.headers.get("Accept-Encoding", "Missing")
    UserAgnets = [
        "UnityPlayer/6000.2.9f1 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
        "UnityPlayer/2022.3.2f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)"
    ]
    Unityversions = [
        "2022.3.2f1",
        "6000.2.9f1"
    ]
    if not CheckMothershipId(MothershipId):
        PfAuthFailed(f"Invalid MothershipId {MothershipId}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403

    if not CheckMothershipToken(MothershipToken):
        PfAuthFailed(f"Invalid MothershipToken {MothershipToken}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403

    if MotheshipEnvId != "7f3a99dd-5598-4725-98cf-6538d28feb9f":
        PfAuthFailed(f"Incorrect MotheshipEnvId {MotheshipEnvId}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if Accept != "deflate, gzip":
        PfAuthFailed(f"Incorrect Accept-Encoding {Accept}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if UserAgent not in UserAgnets:
        PfAuthFailed(f"Incorrect UserAgent {UserAgent}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if Unityversion not in Unityversions:
        PfAuthFailed(f"Incorrect UnityVersion {Unityversion}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403 

    if Platform != "Quest":
        PfAuthFailed(f"Incorrect Platform {Platform}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not CheckOrgscope(OculusId):
        PfAuthFailed(f"Invalid OrgScopedID {OculusId}", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not CheckNonce(nonce=Nonce, userid=OculusId):
        PfAuthFailed(f"Invalid Nonce", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "No Modding! | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    if not AntiVpn(Ip):
        VpnUserBan("Vpn User Caught LOL", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "Turn Off Your Vpn | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403
    
    UserInfo = CheckOrgscope(OculusId)
    metaUser = UserInfo["alias"]
    orgscope = UserInfo["org_scoped_id"]
    CustomId = f"OCULUS{orgscope}"

    if "SPM" in metaUser:
        PfAuthFailed("SPM User Caught LOL", f"Json: ```{r}```\nIp: {Ip}")
        return jsonify({
            "BanMessage": "Having Gui In Game Code | discord.gg/og-tag",
            "BanExpirationTime": "indefinite"
        }), 403

    

    pfreq = requests.post(
        url=f"https://{PfInfo.TitleId}.playfabapi.com/Server/LoginWithServerCustomId",
        headers=Headers,
        json={
            "ServerCustomId": CustomId,
            "CreateAccount": True
        },
        timeout=10
    )
    if pfreq.status_code == 200:
        data = pfreq.json().get("data", {})
        SessionTicket = data.get("SessionTicket", 'Missing')
        PlayFabId = data.get("PlayFabId", 'Missing')
        EntityToken = data.get("EntityToken", {}).get("EntityToken","Missing")
        EntityId = data.get("EntityToken", {}).get("Entity", {}).get("Id")
        EntityType = data.get("EntityToken", {}).get("Entity", {}).get("Type")
        z = CheckPlayFabId(PlayFabId)
        AccountCreation = z["data", {}]["UserInfo", {}]["Created"]
        PfAuthSuccessNewUpd(    
            Orgscope=orgscope,
            OculusId=OculusId,
            PlayFabId=PlayFabId,
            EntityToken=EntityToken,
            SessionTicket=SessionTicket,
            Platform=Platform,
            MothershipId=MothershipId,
            MothershipToken=MothershipToken,
            AccountCreationTime=AccountCreation
        )
        return jsonify({
            "AccountCreationIsoTimestamp": AccountCreation,
            "PlayFabId": PlayFabId,
            "SessionTicket": SessionTicket,
            "EntityId": EntityId,
            "EntityType": EntityType,
            "EntityToken": EntityToken
        }), 200
    else:
        if pfreq.status_code == 403:
            da = pfreq.json()
            if da.get("errorCode") == 1002:
                Details = da.get("errorDetails", {})
                Reason = next(iter(Details))
                Expiration = next(iter(Details[Reason]))
                return jsonify({
                'BanMessage': Reason,
                'BanExpirationTime': Expiration
            }), 403
            else:
                if pfreq.status_code == 429:
                    PfAuthFailed("Too Many Requests To Join", d=None)
                    return "",404




@app.route("/api/photon", methods=["POST"])
def Jaaa():
    r = request.get_json()
    AppId = r.get("AppId")
    AppVersion = r.get("AppVersion")
    Ticket = r.get("Ticket")
    Token = r.get("Token")
    Nonce = r.get("Nonce")
    Platform = r.get("Platform")
    PlayFabId = Ticket.split("-")[0]

    if Platform != "Quest": 
        FailedPhotonAuth("Incorrect Platform", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    if not CheckSessionTicket(Ticket):
        FailedPhotonAuth("Invalid SessionTicket", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    if AppId != "42638":
        FailedPhotonAuth("Incorrect AppId", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    A = CheckPlayFabId(PlayFabId)
    CustomId = A["data"]["UserInfo"]["ServerCustomIdInfo"]["CustomId"]
    orgscope = CustomId.replace("OCULUS", "")
    az = CheckOrgscope(orgscope)
    OculusId = az["id"]
    MetaUser = az["alias"]

    
    return jsonify({
        "ResultCode": 1, 
        "UserId": PlayFabId
    })

def FailedPhotonAuth(title: str, d: str):
    r = requests.post(
        url="https://discord.com/api/webhooks/1494841223385710652/WLJ7-AtgnpwsYMCFysSIISUM0k060n08RpGaQrvUlNO34Yrx4DY-vhjy1tIZz8nzklLJ",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "embeds": [
                {
                    "title": title, 
                    "description": d,
                    "color": 0x8B0000
                }
            ],
            "attachments": []
        }
    )

@app.route("/api/photon/newerupds", methods=["POST"])
def J():
    r = request.get_json()
    AppId = r.get("AppId")
    AppVersion = r.get("AppVersion")
    Ticket = r.get("Ticket")
    Token = r.get("Token")
    Nonce = r.get("Nonce")
    Platform = r.get("Platform")
    
    PlayFabId = Ticket.split("-")[0]

    if Platform != "Quest": 
        FailedPhotonAuth("Incorrect Platform", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    if not CheckSessionTicket(Ticket):
        FailedPhotonAuth("Invalid SessionTicket", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    if AppId != "42638":
        FailedPhotonAuth("Incorrect AppId", f"Json: ```{r}```")
        return jsonify({ 
            "ResultCode": 2, 
            "Message": "Authentication failed" 
        }), 401
    A = CheckPlayFabId(PlayFabId)
    CustomId = A["data"]["UserInfo"]["ServerCustomIdInfo"]["CustomId"]
    orgscope = CustomId.replace("OCULUS", "")
    az = CheckOrgscope(orgscope)
    OculusId = az["id"]
    MetaUser = az["alias"]

    
    return jsonify({
        "ResultCode": 1, 
        "UserId": PlayFabId
    })

@app.route("/i/api/ConsumeOculusIAP", methods=["POST", "GET"])
def consumeoculusiap():
    getdata2 = request.get_json()

    accessToken = getdata2.get("userToken")
    userId = getdata2.get("userID")
    playFabId = getdata2.get("playFabId")
    nonce = getdata2.get("nonce")
    platform = getdata2.get("platform")
    sku = getdata2.get("sku")
    debugParams = getdata2.get("debugParemeters")
    if not CheckPlayFabId(playFabId):
        return "",401
    if not CheckOrgscope(userId):
        return "",401
    if not CheckNonce(nonce, userId):
        return "",401
    if platform != "Quest":
        return "",401

    req = requests.post(
        url=f"https://graph.oculus.com/9902832343082682/consume_entitlement?access_token=OC|9902832343082682|6a97549beb83db376ad5633c976fa604&sku={sku}&user_id={userId}",
        headers={"content-type": "application/json"}
    )

    return jsonify({"success":True})


@app.route("/v2/player/client/auth/begin/QUEST")
def Begin():
    r = request.get_json()
    h = request.headers
    UserId = r.get("UserId", "Missing")
    Ip = h.get("X-Real-Ip")
    EnvId = h.get("X-Mothership-Env-Id", "Missing")
    MothershipTitleId = h.get("X-Mothership-Title-Id", "Missing")
    DevId = h.get("X-Mothership-Deployment-Id", "Missing")
    SdkVersion = h.get("X-Mothership-Sdk-Version", "Missing")
    SdkVersions = [
        "v2025.8.28-1" #add more when u do older upds/newer
    ]
    Dep = [
        "ac205083-a206-4682-9f9d-92c58333c4d1",
        "9f6a6a0d-aeda-4896-9c29-5cadfb213d6b"
    ]
    if MothershipTitleId != "f3e9fb19":
        FailedMothership("Invalid Header, TitleId", f"```UserId: {UserId}\nHeader: {MothershipTitleId}\nIp: {Ip}```")
        return "",404
    if DevId not in Dep:
        FailedMothership("Invalid Header, DeploymentID", f"```UserId: {UserId}\nHeader: {DevId}\nIp: {Ip}```")
        return "",404
    if SdkVersion not in SdkVersions:
        FailedMothership("Invalid Header, SdkVersion", f"```UserId: {UserId}\nHeader: {SdkVersion}\nIp: {Ip}```")
        return "",404
    if EnvId != "7f3a99dd-5598-4725-98cf-6538d28feb9f":
        FailedMothership("Invalid Header, EnvId", f"```UserId: {UserId}\nHeader: {EnvId}\nIp: {Ip}```")
        return "",404
    if not CheckOrgscope(UserId):
        FailedMothership("Invalid UserId", f"```UserId: {UserId}\nIp: {Ip}```")
        return "",404
    AttestationNonce = GenerateChallangeNonce()
    SuccessBegin("Success Begin", f"```UserId: {UserId}\nChallengeNonce: {AttestationNonce}```")
    return jsonify({
        "AttestationNonce": AttestationNonce
    }), 201

@app.route("/v2/player/client/auth/complete/QUEST")
def Complete():
    r = request.get_json()
    h = request.headers
    UserId = r.get("UserId", "Missing")
    AttestationToken = r.get("AttestationToken", "Missing")
    MetaNonce = r.get("MetaNonce", "Missing")
    Ip = h.get("X-Real-Ip")
    EnvId = h.get("X-Mothership-Env-Id", "Missing")
    MothershipTitleId = h.get("X-Mothership-Title-Id", "Missing")
    DevId = h.get("X-Mothership-Deployment-Id", "Missing")
    SdkVersion = h.get("X-Mothership-Sdk-Version", "Missing")
    SdkVersions = [
        "v2025.8.28-1" #add more when u do older upds/newer
    ]
    Dep = [
        "ac205083-a206-4682-9f9d-92c58333c4d1",
        "9f6a6a0d-aeda-4896-9c29-5cadfb213d6b"
    ]
    if MothershipTitleId != "f3e9fb19":
        FailedMothership("Invalid Header, TitleId", f"```UserId: {UserId}\nHeader: {MothershipTitleId}\nIp: {Ip}```")
        return "",404
    if DevId not in Dep:
        FailedMothership("Invalid Header, DeploymentID", f"```UserId: {UserId}\nHeader: {DevId}\nIp: {Ip}```")
        return "",404
    if SdkVersion not in SdkVersions:
        FailedMothership("Invalid Header, SdkVersion", f"```UserId: {UserId}\nHeader: {SdkVersion}\nIp: {Ip}```")
        return "",404
    if EnvId != "7f3a99dd-5598-4725-98cf-6538d28feb9f":
        FailedMothership("Invalid Header, EnvId", f"```UserId: {UserId}\nHeader: {EnvId}\nIp: {Ip}```")
        return "",404
    if not CheckOrgscope(UserId):
        FailedMothership("Invalid UserId", f"```UserId: {UserId}\nIp: {Ip}```")
        return "",401
    if not CheckAttestation(AttestationToken):
        FailedMothership(f"Integrity Check Failed For {UserId}", f"```UserId: {UserId}\nToken: {AttestationToken}\nIp: {Ip}```")
        return "",401
    
    C = CheckAttestation(AttestationToken)
    Claims = C["claims"]
    Decoded = b64Decode(Claims)
    John = json.loads(Decoded)
    Expiration = John.get("request_details", {}).get("exp")
    TimeStamp = John.get("request_details", {}).get("timestamp")
    AppIntegrity = John.get("app_state", {}).get("app_integrity_state")
    Sha256 = John.get("app_state", {}).get("package_cert_sha256_digest")[0]
    Package = John.get("app_state", {}).get("package_id")
    VersionCode = John.get("app_state", {}).get("version")
    Hwid = John.get("device_state", {}).get("unique_id")
    DeviceIntegrity = John.get("device_state", {}).get("device_integrity_state")
    Token = str(GenToken())
    PlayerIda = "OGTAG-" + str(uuid.uuid4())
    Uin = CheckOrgscope(UserId)
    MetaUser = Uin["alias"]
    orgscope = Uin["org_scoped_id"]

    if CheckIfbanned(hwid=Hwid):
        BannedLogings("Hwid Banned User Logged In", f"```UserId: {UserId}\nHwid: {Hwid}\nMetaUser: {MetaUser}```")
        return "",401
    
    if AppIntegrity != "StoreRecognized" or Sha256 != "6dbb3f10520bf5a89fa70f0e414eb66497f3c44db0e6727a0f598109bf7c13d5" or Package != "com.SystemFrs.OGTag" or VersionCode != "yourversioncode" or DeviceIntegrity != "Advanced":
        r = requests.post(
            url="https://discord.com/api/webhooks/1479943915892244621/0BhqT8K-RY-s4sydMhO6yiXv6n6YpIlNH__60uQXbYXJ_A6jiYCpPHFm9r61F_2n-UN3",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "embeds": [
                    {
                        "title": "Apk User",
                        "color": 0x8B0000,
                        "fields": [
                            {
                                "name": "UserId",
                                "value": f"```{UserId}```"
                            },
                            {
                                "name": "Hwid",
                                "value": f"```{Hwid}```"
                            },
                            {
                                "name": "MetaUser",
                                "value": f"```{MetaUser}```"
                            },
                            {
                                "name": "OrgScopedID",
                                "value": f"```{orgscope}```"
                            },
                            {
                                "name": "Sha256",
                                "value": f"```{Sha256}```"
                            },
                            {
                                "name": "PackageName",
                                "value": f"```{Package}```"
                            }
                        ]
                    }
                ],
                "attachments": []
            },
            timeout=10
        )
        return "",401
    PlayerId = AddToDb(PlayerIda, Token, UserId, Hwid)
    SuccessComplete("Success Complete", f"```UserId: {UserId}\nToken: {Token}\nPlayerId: {PlayerId}\nHwid: {Hwid}\nMetaUser: {MetaUser}\nOrgScopedID: {orgscope}```", Id=PlayerId)
    return jsonify({
        "ExternalProviderId": UserId,
        "ExternalProviderUsername": MetaUser,
        "IsPrimaryId": True,
        "PlayerId": PlayerId,
        "Tags": None,
        "Token": Token,
        "ExpirationTime": Expiration
    }), 201
