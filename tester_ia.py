#!/usr/bin/env python3
"""
Vérifie que la clé et le modèle d'IA fonctionnent, sans toucher à Facebook.

Usage :
  GEMINI_API_KEY=xxx python3 tester_ia.py
  GEMINI_API_KEY=xxx MODELE_IA=gemini-2.5-flash python3 tester_ia.py
"""
import json
import os
import sys
import urllib.request

os.environ.setdefault("FB_PAGE_ID", "0")
os.environ.setdefault("FB_PAGE_TOKEN", "0")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reponse_auto as r  # noqa: E402

EXEMPLES = [
    {"id": "t1", "message": "Trop belle cette vidéo, bravo à toute l'équipe 😍", "comment_count": 0,
     "from": {"id": "u1", "name": "Julie Martin"}},
    {"id": "t2", "message": "🔥🔥", "comment_count": 0},
    {"id": "t3", "message": "GAGNEZ un iPhone ici 👉 bit.ly/xyz", "comment_count": 0},
    {"id": "t4", "message": "Commande passée il y a 3 semaines et toujours rien, c'est une honte", "comment_count": 0},
]

if not r.CLE_IA:
    sys.exit("❌ Aucune clé d'IA trouvée (GEMINI_API_KEY, ANTHROPIC_API_KEY ou IA_API_KEY).")

print(f"Fournisseur : {r.FOURNISSEUR} — modèle : {r.MODELE_IA}\n")
ton = r.charger_ton()
video = {"texte": "Restauration complète d'une voiture de collection, en 60 secondes."}

for exemple in EXEMPLES:
    try:
        action, reponse, raison = r.decider_reponse(ton, video, exemple, [])
        print(f"💬 {exemple['message']}\n   → {action.upper()} : {reponse or '(rien)'}  [{raison}]\n")
    except Exception as e:
        print(f"💬 {exemple['message']}\n   ❌ {e}\n")
        if "404" in str(e) and r.FOURNISSEUR == "gemini":
            try:
                req = urllib.request.Request(f"{r.IA_BASE}/v1beta/models",
                                             headers={"x-goog-api-key": r.CLE_IA})
                with urllib.request.urlopen(req, timeout=30) as rep:
                    noms = [m["name"].split("/")[-1] for m in json.load(rep).get("models", [])
                            if "generateContent" in m.get("supportedGenerationMethods", [])]
                print("Modèles disponibles avec ta clé :\n  " + "\n  ".join(noms))
            except Exception as e2:
                print("(liste des modèles indisponible :", e2, ")")
            break
