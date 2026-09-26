# Réponses automatiques aux commentaires Facebook — guide pas à pas

Ce système répond tout seul, au nom de ta Page, aux commentaires laissés sous tes vidéos de DS.
Toutes les 10 minutes environ, il lit les nouveaux commentaires, demande à l'IA Claude une réponse dans le ton
de ta Page (fichier `ton_de_la_page.md`), puis la publie en prenant son temps, comme un humain.

**Durée de l'installation :** environ 1 h 30 la première fois.
**Coût :** environ 30 à 45 $ par mois pour 400 à 700 commentaires par jour (IA Claude). Facebook et GitHub sont gratuits.

**Ce qu'il te faut :**
- ton Mac ;
- le compte Facebook qui est administrateur de ta Page ;
- une adresse e-mail ;
- une carte bancaire (pour l'IA).

**Contenu du dossier :**

| Fichier | Rôle |
|---|---|
| `reponse_auto.py` | Le programme principal (ne pas modifier) |
| `ton_de_la_page.md` | Le « cerveau » : ton, histoire de la DS, fiche de ta voiture, exemples. **À personnaliser** |
| `obtenir_token.py` | Sert à obtenir le jeton de ta Page (étapes 4 et 14) |
| `tester_ia.py` | Vérifie que la clé de l'IA fonctionne (étape 6) |
| `.github/workflows/reponses-facebook.yml` | Lance le programme toutes les 10 minutes |
| `.github/workflows/garder-actif.yml` | Empêche GitHub de mettre le système en pause après 60 jours |

> 🔒 **Règle d'or :** le jeton Facebook et la clé Claude sont comme des mots de passe.
> Ne les envoie à personne, ne les colle nulle part ailleurs que là où ce guide le dit.

---

## Étape 1 — Préparer le dossier (10 min)

1. Télécharge le fichier `reponses-facebook.zip`.
2. Double-clique dessus : un dossier `reponses-facebook` apparaît. Range-le sur ton **Bureau**.
3. Le fichier `ton_de_la_page.md` est déjà rempli pour la Page Mémoire Auto : rien à modifier.
   Tu pourras l'ajuster plus tard directement sur GitHub (étape 11).

> 🎵 **Musique :** l'IA ne peut pas savoir quelle musique passe dans ta vidéo, même quand elle vient de la
> bibliothèque musicale de Facebook : l'accès officiel utilisé par le programme ne transmet pas cette information.
> Par défaut, elle ne répond donc pas aux questions sur la musique. Si un jour tu veux qu'elle réponde pour une vidéo précise, ajoute à la fin
> de la description Facebook une ligne `Musique : Titre – Artiste`.

## Étape 2 — Ouvrir le Terminal au bon endroit (5 min)

Le Terminal est une application de ton Mac qui permet de lancer les petits programmes du dossier.

1. Appuie sur `Cmd + Espace`, tape **Terminal**, puis appuie sur **Entrée**. Une fenêtre avec du texte s'ouvre.
2. Tape `cd` suivi d'**un espace** (n'appuie pas encore sur Entrée).
3. Fais glisser le dossier `reponses-facebook` depuis ton Bureau jusque dans la fenêtre du Terminal : son chemin s'écrit tout seul.
4. Appuie sur **Entrée**.
5. Tape `python3 --version` puis **Entrée**.
   - Si tu vois `Python 3.` suivi de chiffres : parfait.
   - Si une fenêtre te propose d'installer les « outils de ligne de commande » : clique sur **Installer**, attends la fin
     (5 à 15 min), puis retape `python3 --version`.

> Garde cette fenêtre du Terminal ouverte : elle servira aux étapes 4 et 6.
> Si tu la fermes, recommence simplement les points 1 à 4 de cette étape.

## Étape 3 — Créer l'app Meta (15 min)

Une « app Meta » est l'autorisation officielle qui permet au programme de répondre au nom de ta Page.

1. Va sur <https://developers.facebook.com> et connecte-toi avec le compte Facebook **administrateur de ta Page**.
2. Si c'est ta première visite, clique sur **Commencer** et suis les écrans (accepter les conditions, confirmer ton
   e-mail ou ton téléphone).
3. Clique sur **Mes apps** (en haut à droite), puis sur **Créer une app**.
4. Nom de l'app : `Réponses DS`. E-mail de contact : ton e-mail. Clique sur **Suivant**.
5. Dans la liste des cas d'usage, choisis **« Gérer tout sur votre Page »**. Clique sur **Suivant**.
6. Si on te demande un « portefeuille business » : choisis **ne pas en associer pour l'instant**. Clique sur **Suivant**,
   puis **Créer l'app** (ton mot de passe Facebook peut être demandé).
7. Dans le tableau de bord de l'app, ouvre le cas d'usage **« Gérer tout sur votre Page »** → **Personnaliser** /
   **Autorisations**, et vérifie que ces 4 autorisations sont présentes (clique sur **Ajouter** si l'une manque) :
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_read_user_content`
   - `pages_manage_engagement`
8. Dans le menu de gauche : **Paramètres de l'app** → **Général**.
   - Copie l'**ID de l'app** dans l'app **Notes** de ton Mac.
   - À côté de **Clé secrète**, clique sur **Afficher** (mot de passe demandé), puis copie-la aussi dans Notes.

> Meta change souvent le nom de ses menus. Si un libellé est différent, cherche l'option qui parle de « Pages ».

## Étape 4 — Obtenir le jeton de ta Page (10 min)

Le jeton est la « clé » qui permet de publier au nom de ta Page.

1. Va sur <https://developers.facebook.com/tools/explorer>.
2. À droite, dans **Application Meta**, choisis **Réponses DS**.
3. Dans **Utilisateur ou Page**, choisis **Obtenir un jeton d'accès utilisateur** (*User Token*).
4. Dans **Autorisations**, ajoute une par une les 4 autorisations de l'étape 3.
5. Clique sur **Generate Access Token**. Une fenêtre Facebook s'ouvre :
   - clique sur **Continuer** ;
   - **coche ta Page** (important) ;
   - valide jusqu'au bout.
6. De retour sur la page, clique sur l'icône de copie à côté du jeton (une longue suite de lettres qui commence par `EAA`).
7. Retourne dans le **Terminal** (étape 2), tape `python3 obtenir_token.py` puis **Entrée**. Le programme te demande :
   - l'**ID de l'app** → colle-le (`Cmd + V`) puis **Entrée** ;
   - la **clé secrète** → colle-la puis **Entrée**. *Rien ne s'affiche quand tu colles : c'est normal, c'est masqué* ;
   - le **jeton** → colle-le puis **Entrée** (masqué aussi).
8. Le programme affiche un bloc pour chacune de tes Pages. Pour **ta Page** :
   - copie la valeur de `FB_PAGE_ID` dans Notes ;
   - copie la valeur de `FB_PAGE_TOKEN` dans Notes ;
   - vérifie que la ligne **Expiration** indique **jamais ✅**.

> Si tu vois « Erreur Facebook » : le jeton de l'étape 4 dure une heure seulement. Refais les points 5 à 7.

## Étape 5 — Créer ton compte pour l'IA Claude (10 min)

1. Va sur <https://platform.claude.com> et crée un compte avec ton e-mail.
2. Va dans **Settings** (Paramètres) → **Billing** (Facturation) :
   - ajoute ta carte bancaire ;
   - achète **20 $** de crédits pour commencer. Plus tard, tu pourras activer la recharge automatique.
3. Va dans **Limits** (Limites) et fixe une **limite de dépense mensuelle de 60 $**. C'est ta sécurité : même en cas de
   vidéo très virale, tu ne dépenseras jamais plus.
4. Va dans **API Keys** → **Create Key**. Nom : `reponses-facebook`. Clique sur **Create**.
5. **Copie immédiatement la clé** (elle commence par `sk-ant-`) dans Notes : elle ne sera plus jamais affichée.

## Étape 6 — Vérifier que l'IA fonctionne (2 min)

1. Retourne dans le **Terminal**.
2. Tape la ligne suivante **en remplaçant `sk-ant-XXXX` par ta clé**, puis appuie sur **Entrée** :

   ```
   ANTHROPIC_API_KEY=sk-ant-XXXX MODELE_IA=claude-haiku-4-5-20251001 python3 tester_ia.py
   ```

3. Tu dois voir 4 commentaires d'exemple, chacun suivi de la réponse de l'IA.
   Ces exemples ne parlent pas de DS : ce test vérifie seulement que ta clé fonctionne.
   - `IA (401)` → la clé est mal copiée : recommence en la recollant.
   - `IA (400)` qui parle de crédits → ton achat de crédits (étape 5) n'est pas encore passé.

## Étape 7 — Créer ton compte GitHub (5 min)

GitHub est le service gratuit qui va faire tourner le programme à ta place, même quand ton Mac est éteint.

1. Va sur <https://github.com> → **Sign up**.
2. Crée ton compte (e-mail, mot de passe, nom d'utilisateur) et confirme ton e-mail.

## Étape 8 — Mettre le programme sur GitHub (10 min)

1. Sur GitHub, clique sur le **+** en haut à droite → **New repository**.
2. **Repository name** : `reponses-ds`.
3. Coche **Public**. (C'est ce qui rend le système gratuit ; tes clés resteront secrètes quoi qu'il arrive.)
4. Clique sur **Create repository**.
5. Sur la page qui s'affiche, clique sur le lien **uploading an existing file**.
6. Sur ton Mac, ouvre le dossier `reponses-facebook` dans le Finder et appuie sur `Cmd + Maj + .` (point) :
   le dossier caché `.github` apparaît en grisé.
7. Sélectionne **tout** le contenu du dossier (`Cmd + A`) et fais-le glisser dans la page GitHub.
8. Attends que tous les fichiers soient listés, puis clique sur le bouton vert **Commit changes**.
9. **Vérification :** sur la page du dépôt, clique sur le dossier `.github`, puis `workflows`. Tu dois y voir
   `reponses-facebook.yml` et `garder-actif.yml`.

   **Si le dossier `.github` n'apparaît pas** (certains navigateurs refusent les dossiers cachés) :
   1. reviens à la page du dépôt et clique sur **Add file** → **Create new file** ;
   2. dans la case du nom, tape exactement `.github/workflows/reponses-facebook.yml`
      (les `/` créent les dossiers tout seuls) ;
   3. sur ton Mac, ouvre `reponses-facebook.yml` avec TextEdit (clic droit → Ouvrir avec → TextEdit),
      fais `Cmd + A` puis `Cmd + C` ;
   4. clique dans la grande zone de texte de GitHub, fais `Cmd + V`, puis **Commit changes** (deux fois si demandé) ;
   5. recommence avec `.github/workflows/garder-actif.yml`.

## Étape 9 — Enregistrer les 3 secrets (5 min)

1. Sur la page de ton dépôt, clique sur l'onglet **Settings** (roue dentée, en haut).
2. Dans le menu de gauche : **Secrets and variables** → **Actions**.
3. Clique sur **New repository secret** et crée ces 3 secrets, un par un (champ **Name**, champ **Secret**,
   puis **Add secret**) :

   | Name | Secret |
   |---|---|
   | `FB_PAGE_ID` | la valeur `FB_PAGE_ID` notée à l'étape 4 |
   | `FB_PAGE_TOKEN` | la valeur `FB_PAGE_TOKEN` notée à l'étape 4 |
   | `ANTHROPIC_API_KEY` | ta clé Claude (`sk-ant-…`) |

   Recopie les noms **exactement** (majuscules et tirets bas compris).
   Ne crée **pas** de secret `GEMINI_API_KEY`.

## Étape 10 — Créer les 6 réglages (5 min)

1. Même écran, clique sur l'onglet **Variables** (à côté de **Secrets**).
2. Clique sur **New repository variable** et crée ces 6 variables, une par une (**Name**, **Value**, puis
   **Add variable**) :

   | Name | Value | À quoi ça sert |
   |---|---|---|
   | `MODELE_IA` | `claude-haiku-4-5-20251001` | le modèle d'IA utilisé |
   | `MAX_REPONSES_PAR_EXECUTION` | `15` | 15 réponses maximum toutes les 10 min (90 par heure) |
   | `PAUSE_PUBLICATION_MIN` | `10` | au moins 10 secondes entre deux réponses |
   | `PAUSE_PUBLICATION_MAX` | `35` | au plus 35 secondes entre deux réponses |
   | `DELAI_MIN_COMMENTAIRE_MINUTES` | `3` | ne jamais répondre moins de 3 minutes après un commentaire |
   | `AGE_MAX_COMMENTAIRE_HEURES` | `72` | ne répondre qu'aux commentaires de moins de 3 jours |

## Étape 11 — Faire un test sans rien publier (10 min)

Tant que la variable `MODE_TEST` n'existe pas (ou vaut `1`), **rien n'est jamais publié** et rien ne tourne tout seul.

1. Clique sur l'onglet **Actions** du dépôt. Si un bouton vert te demande d'activer les workflows, clique dessus.
2. Dans la colonne de gauche, clique sur **Réponses automatiques Facebook**.
3. À droite, clique sur **Run workflow**, laisse « Mode test » à `1`, puis clique sur le bouton vert **Run workflow**.
4. Attends 1 à 3 minutes, puis clique sur l'exécution qui apparaît (ligne en haut de la liste).
5. Dans **Summary**, un tableau montre chaque commentaire récent de tes vidéos et la réponse que l'IA **aurait** publiée.
   Pour plus de détails, clique sur **repondre** puis sur **Répondre aux commentaires**.
6. Relis attentivement. Si quelque chose ne te plaît pas :
   - ouvre `ton_de_la_page.md` sur GitHub → clique sur le **crayon** ✏️ → modifie → **Commit changes** ;
   - relance le test (points 2 à 5).
7. **Si le tableau est vide alors que ta Page a des commentaires récents :** l'app Meta est probablement encore en
   « mode développement ». Va dans le tableau de bord de l'app sur developers.facebook.com et passe-la en mode
   **« En ligne »** (*Live*). Meta demande l'adresse d'une page de **politique de confidentialité** : tu peux écrire
   quelques lignes dans un Google Docs (« Cette application sert uniquement à répondre aux commentaires de ma Page.
   Aucune donnée n'est revendue. »), le partager en « Tous les utilisateurs disposant du lien », et coller ce lien.
   Puis relance le test.

## Étape 12 — Activer les vraies réponses (2 min)

1. **Settings** → **Secrets and variables** → **Actions** → onglet **Variables**.
2. **New repository variable** : Name `MODE_TEST`, Value `0` → **Add variable**.
   (Si `MODE_TEST` existe déjà, clique sur le crayon à côté pour mettre `0`.)
3. C'est parti : dans les 10 à 20 minutes, le système tourne tout seul, jour et nuit, même Mac éteint.

**Pour tout arrêter à n'importe quel moment :** remets `MODE_TEST` à `1`.
Plus rien ne tourne tout seul (et plus rien n'est facturé par l'IA).

## Étape 13 — Surveiller la première semaine (5 min par jour)

- **GitHub → Actions** : ouvre la dernière exécution, étape « Répondre aux commentaires ».
  La dernière ligne indique `X réponse(s), Y like(s) seul(s), Z ignoré(s)`.
  Si les likes et ignorés dépassent 5 % du total, il faudra ajuster `ton_de_la_page.md`.
- **platform.claude.com → Usage** : vérifie la dépense, environ 1 à 1,50 $ par jour pour 400 à 700 commentaires.
- **Ta Page Facebook** : lis quelques réponses publiées chaque jour.
- Supprime de l'app Notes le jeton et la clé une fois que tout fonctionne (ils sont en sécurité dans GitHub).

---

## Étape 14 — Changer de Page (10 min, à chaque nouvelle Page)

Quand une Page a atteint son objectif d'abonnés et que tu veux brancher le système sur une nouvelle Page.
Tout le reste (app Meta, compte Claude, dépôt GitHub, réglages) est **réutilisé tel quel**.

1. **Créer la nouvelle Page** sur Facebook, **avec le même compte Facebook** (tu dois en être administrateur).
2. **Mettre le système en pause** : GitHub → **Settings** → **Secrets and variables** → **Actions** → onglet
   **Variables** → crayon à côté de `MODE_TEST` → valeur `1` → **Update variable**.
3. **Obtenir le jeton de la nouvelle Page** :
   1. va sur <https://developers.facebook.com/tools/explorer>, choisis l'app **Réponses DS** ;
   2. **Obtenir un jeton d'accès utilisateur**, vérifie que les 4 autorisations sont bien listées ;
   3. **Generate Access Token** → dans la fenêtre Facebook, **coche la nouvelle Page** → valide jusqu'au bout ;
   4. copie le jeton ;
   5. dans le Terminal (refais l'étape 2 si besoin), tape `python3 obtenir_token.py` et colle l'ID de l'app,
      la clé secrète (toujours dans Notes, ou à retrouver dans Paramètres de l'app → Général) et le jeton ;
   6. dans le bloc de la **nouvelle Page**, copie `FB_PAGE_ID` et `FB_PAGE_TOKEN`, et vérifie **Expiration : jamais ✅**.
4. **Remplacer les 2 secrets** : GitHub → **Settings** → **Secrets and variables** → **Actions** → onglet **Secrets** :
   - crayon à côté de `FB_PAGE_ID` → colle le nouvel ID → **Update secret** ;
   - crayon à côté de `FB_PAGE_TOKEN` → colle le nouveau jeton → **Update secret**.
5. **Mettre à jour le fichier de ton** : ouvre `ton_de_la_page.md` sur GitHub → crayon ✏️ → remplace le nom de la Page
   (première section). Si la nouvelle Page montre une autre voiture, adapte aussi la section « La voiture des vidéos ».
   → **Commit changes**.
6. **Tester** : refais l'étape 11 (test sans rien publier) sur la nouvelle Page.
7. **Réactiver** : remets `MODE_TEST` à `0` (crayon → `0` → **Update variable**).

Dès ce moment, l'IA répond sur la nouvelle Page et **ne touche plus du tout à l'ancienne**.
La mémoire des commentaires déjà traités se nettoie toute seule au bout de 14 jours : rien à faire.

> Conseil : sur chaque nouvelle Page, publie de nouvelles vidéos (ou des montages différents). Facebook peut réduire la
> diffusion des vidéos identiques republiées d'une Page à l'autre.

---

## En cas de problème

| Ce que tu vois dans le journal (Actions) | Solution |
|---|---|
| `code 190` / jeton invalide | Le jeton a été invalidé (mot de passe Facebook changé, rôle d'admin perdu…). Refais l'étape 4, puis mets à jour le secret `FB_PAGE_TOKEN` (étape 14, point 4) |
| `code 10` ou `code 200` / permission | Une des 4 autorisations manque : refais l'étape 4 en les ajoutant toutes |
| `0 vidéo(s) récente(s)` | Vérifie le secret `FB_PAGE_ID`. Pour tester sur toutes tes publications, crée la variable `VIDEOS_SEULEMENT` = `0` |
| Des commentaires existent mais le tableau est vide | Passe l'app Meta en mode « En ligne » (étape 11, point 7) |
| `IA (401)` | Clé Claude incorrecte : recrée une clé (étape 5) et mets à jour le secret `ANTHROPIC_API_KEY` |
| `IA (400)` qui parle de crédits ou de facturation | Plus de crédits ou limite de dépense atteinte : va dans Billing / Limits sur platform.claude.com |
| `Quota de l'IA atteint` | Trop d'appels d'un coup : rien à faire, la suite est traitée au passage suivant |
| Aucune exécution automatique n'apparaît | Vérifie que `MODE_TEST` vaut bien `0`. GitHub peut aussi avoir 5 à 15 min de retard aux heures chargées |
| E-mail de GitHub « workflow disabled » | Onglet Actions → clique sur le workflow concerné → **Enable workflow** |

## Réglages avancés (facultatif)

À créer comme **variables** (même endroit que `MODE_TEST`) :

| Variable | Défaut | Effet |
|---|---|---|
| `AGE_MAX_VIDEO_JOURS` | `30` | Surveille les vidéos publiées depuis moins de N jours |
| `LIKER_COMMENTAIRES` | `1` | `0` = la Page ne like plus les commentaires |
| `VIDEOS_SEULEMENT` | `1` | `0` = répond aussi sous les photos et publications texte |
| `PAUSE_ENTRE_APPELS_IA` | `0` | Pause (en secondes) entre deux appels à l'IA |

Pour changer la fréquence de passage, modifie la ligne `cron` dans `.github/workflows/reponses-facebook.yml`
(`*/10 * * * *` = toutes les 10 minutes).
