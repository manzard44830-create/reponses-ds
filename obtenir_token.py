#!/usr/bin/env python3
"""
Transforme un jeton utilisateur de courte durée (Graph API Explorer) en jeton de Page
de longue durée, et affiche l'identifiant de chaque Page que tu gères.

Usage :
  python3 obtenir_token.py
(le script te demande l'ID de l'app, la clé secrète de l'app et le jeton de courte durée)
"""
import getpass
import json
import urllib.error
import urllib.parse
import urllib.request

VERSION = "v25.0"


def get(chemin, params):
    url = f"https://graph.facebook.com/{VERSION}/{chemin}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit("Erreur Facebook : " + e.read().decode())


app_id = input("ID de l'app Meta : ").strip()
app_secret = getpass.getpass("Clé secrète de l'app (masquée) : ").strip()
jeton_court = getpass.getpass("Jeton utilisateur de Graph API Explorer (masqué) : ").strip()

long = get("oauth/access_token", {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": jeton_court,
})["access_token"]

pages = get("me/accounts", {"access_token": long, "fields": "id,name,access_token,tasks"}).get("data", [])
if not pages:
    raise SystemExit("Aucune Page trouvée : vérifie que tu as bien coché ta Page lors de l'autorisation.")

for p in pages:
    print("\n" + "=" * 60)
    print("Page          :", p["name"])
    print("FB_PAGE_ID    :", p["id"])
    print("FB_PAGE_TOKEN :", p["access_token"])
    print("Droits        :", ", ".join(p.get("tasks", [])))
    info = get("debug_token", {"input_token": p["access_token"], "access_token": f"{app_id}|{app_secret}"})
    expire = info.get("data", {}).get("expires_at", 0)
    print("Expiration    :", "jamais ✅" if expire == 0 else f"timestamp {expire} ⚠️")
    print("Permissions   :", ", ".join(info.get("data", {}).get("scopes", [])))
print("\nCopie FB_PAGE_ID et FB_PAGE_TOKEN de ta Page dans les secrets GitHub. Ne partage jamais le jeton.")
