# Mettre le site en ligne

## ⚠️ À lire avant tout : ne pas écraser le site actuel

`al-fissah.com` héberge aujourd'hui une application complète : espace étudiant,
connexion, planning, paiements Stripe, commandes. **Ce site-ci ne remplace que les
pages de présentation.** Si vous le déposez à la racine de `al-fissah.com`, vos élèves
perdent l'accès à leur espace et les paiements s'arrêtent.

Trois façons de procéder, de la plus sûre à la plus engageante :

**A. Sous-domaine de test (recommandé pour commencer)**
Publiez sur `nouveau.al-fissah.com`. Le site actuel continue de tourner sans y toucher.
Vous montrez le résultat autour de vous, vous corrigez tranquillement, et vous basculez
plus tard quand tout vous convient.

**B. Adresse temporaire de l'hébergeur**
Netlify ou Cloudflare vous donnent une adresse du type `al-fissah.netlify.app`,
immédiatement, sans toucher au nom de domaine. Idéal pour un premier essai.

**C. Remplacement du site public**
Seulement quand vous êtes décidé, et à condition de garder les chemins de
l'application (`/fr/login`, `/fr/register`, `/fr/commander/...`) qui doivent continuer
de pointer vers l'application existante. Demande l'aide de la personne qui gère
l'application actuelle.

---

## Option 1 — Netlify (gratuit, le plus simple, aucune installation)

1. Créez un compte sur **netlify.com** (gratuit).
2. Sur le tableau de bord, cherchez la zone **« Deploy manually »** / « Drag and drop ».
3. **Glissez-y le dossier `site` en entier** (pas le zip, le dossier).
4. En une minute, le site est en ligne sur une adresse `xxx.netlify.app`.
5. Pour votre propre adresse : *Domain settings → Add a domain* → `nouveau.al-fissah.com`.
   Netlify vous donne une valeur à ajouter chez votre registrar (un enregistrement CNAME).
   Le certificat HTTPS est installé automatiquement.

Pour mettre à jour plus tard : reglissez le dossier, cela écrase la version précédente.
Le fichier `netlify.toml` et `_redirects` sont déjà dans le dossier : pages 404 par
langue, en-têtes de sécurité et mise en cache sont configurés.

## Option 2 — Cloudflare Pages (gratuit, même principe)

Compte sur **dash.cloudflare.com** → *Workers & Pages* → *Create* → *Pages* →
*Upload assets* → glissez le dossier `site`. Le fichier `_redirects` est reconnu tel quel.

## Option 3 — Hébergement classique (OVH, o2switch, Hostinger, LWS, IONOS…)

Si vous avez déjà un hébergement mutualisé avec le domaine :

1. Connectez-vous en **FTP** (FileZilla) ou via le gestionnaire de fichiers de l'hébergeur.
2. Placez-vous dans le dossier public : `www/`, `public_html/` ou `httpdocs/` selon
   l'hébergeur — **ou dans le sous-dossier du sous-domaine** si vous suivez l'option A.
3. Envoyez **le contenu** du dossier `site` (pas le dossier lui-même) : `index.html`,
   `assets/`, `ar/`, `en/`, `es/`, `de/`, `404.html`, `sitemap.xml`, `robots.txt`,
   `.htaccess`.
4. Activez le certificat SSL gratuit (Let's Encrypt) dans le panneau de l'hébergeur.

Le fichier `.htaccess` fourni s'occupe du reste : HTTPS forcé, page 404, compression,
cache.

---

## Ce qu'il ne faut PAS envoyer sur le serveur

Ces fichiers servent à fabriquer le site, pas à le faire tourner :

```
build.py          lang/          pics.json       part_classroom.html
README.md         CONSULTER-EN-LOCAL.md          MISE-EN-LIGNE.md
demarrer-windows.bat            demarrer-mac-linux.command
```

Gardez-les précieusement sur votre ordinateur : sans eux, vous ne pourrez plus
régénérer les 5 langues d'un coup. Le `.htaccess` fourni les bloque déjà au cas où.

---

## Après la mise en ligne : la liste de contrôle

- [ ] Compléter les **mentions légales** (adresse du siège, NM Business ID, agent
      enregistré, directeur de publication, hébergeur) — obligatoire.
- [ ] Brancher les **formulaires** sur une vraie adresse d'envoi (voir plus bas).
- [ ] Remplacer le **logo provisoire** `assets/logo.svg` par le vôtre.
- [ ] Vérifier le lien **« Se connecter »** : il pointe vers `al-fissah.com/fr/login`.
- [ ] Vérifier les boutons **« Choisir »** des tarifs : ils mènent au formulaire d'essai.
      Pour envoyer vers la commande en ligne, remplacez par les adresses de
      l'application existante.
- [ ] Déclarer le site dans **Google Search Console** et y soumettre `sitemap.xml`.
- [ ] Vérifier `SITE` en haut de `build.py` : l'adresse qui y figure sert aux balises
      canoniques et au sitemap. Si vous publiez sur un sous-domaine, mettez-le à jour
      et relancez `python3 build.py`.

---

## Brancher les formulaires (5 minutes)

Aujourd'hui, les formulaires ouvrent la messagerie du visiteur. Pour recevoir les
demandes directement sur `c.alfissah@gmail.com` :

1. Allez sur **web3forms.com** (gratuit, sans compte à créer).
2. Saisissez `c.alfissah@gmail.com` → vous recevez une **clé d'accès** par e-mail.
3. Ouvrez `assets/main.js`, ligne ~142, et remplacez :
   ```js
   const FORM_ENDPOINT="";
   ```
   par :
   ```js
   const FORM_ENDPOINT="https://api.web3forms.com/submit";
   const FORM_KEY="votre-cle-recue-par-email";
   ```
4. Renvoyez le fichier sur le serveur.

Les demandes arrivent alors dans votre boîte, et le visiteur voit une confirmation
directement sur la page. Un champ anti-spam invisible est déjà en place.

*(Formspree et Getform fonctionnent de la même manière si vous préférez.)*
