# Mettre le site en ligne

## Bascule vers al-fissah.com (21/11/2026) — la vitrine remplace l'ancien site

La vitrine quitte al-fissah.fr pour **al-fissah.com** ; l'ancien site (Laravel, serveur OVH
193.70.85.109) disparaît de cette adresse. **Les comptes ne changent pas** : etudiant /
enseignant / gestion.al-fissah.com restent sur la plateforme (Vercel), identifiants inchangés.
Ce dépôt est déjà prêt (`site.conf` : `site=https://al-fissah.com`, `preview=non` ; `.htaccess` :
al-fissah.fr et www → al-fissah.com, anciens liens de l'ancien site → bonne page).

⚠ **blog.al-fissah.com et livres.al-fissah.com tournent sur le même serveur OVH** : on ne coupe
pas ce serveur, on change seulement l'adresse `al-fissah.com` (et `www`).

Dans cet ordre :

1. **Export final de l'ancien site** : juste APRÈS l'étape 5 (le changement d'adresse fige l'ancien
   site ; sa base reste sur le serveur OVH, lisible par SSH).
2. **al-fissah.com a son propre hébergement LWS** (constaté le 21/11/2026). Panel LWS →
   al-fissah.com → *Gérer* → **FTP** : relever le serveur, l'identifiant, le mot de passe, et le
   dossier du site (souvent `/` ou `/htdocs/`). Noter aussi l'**adresse IP** de cet hébergement.
3. **GitHub → dépôt `al-fissah-site` → Settings → Secrets and variables → Actions** :
   secrets `FTP_HOST_COM`, `FTP_USERNAME_COM`, `FTP_PASSWORD_COM` ; onglet *Variables* :
   `FTP_DOSSIER_COM` = le dossier relevé (avec `/` au début et à la fin).
4. **Fusionner la demande de fusion de ce dépôt** sur `main` : la mise en ligne publie la vitrine
   dans l'hébergement d'al-fissah.com (invisible tant que le DNS pointe sur OVH) ET sur al-fissah.fr,
   qui renvoie dès lors vers al-fissah.com (encore l'ancien site jusqu'à l'étape 5 : faire 4 et 5
   à la suite).
5. **Panel LWS → Zone DNS d'al-fissah.com** — ne modifier QUE ces lignes :
   - `@` et `www`, type **A** : `193.70.85.109` → l'adresse IP de l'hébergement al-fissah.com (étape 2) ;
   - `@` et `www`, type **AAAA** : supprimer `2001:41d0:302:2200::59c5` (ou mettre l'IPv6 LWS de l'hébergement).
   **Ne pas toucher** : MX, `mail`, TXT (SPF, DKIM, Amazon SES), `etudiant`, `enseignant`,
   `gestion` (Vercel), `cours`, `blog`, `livres`.
   Puis, quelques minutes plus tard : **SSL** de l'hébergement al-fissah.com →
   certificat Let's Encrypt pour `al-fissah.com` et `www.al-fissah.com`.
6. Vérifier :
   - `https://al-fissah.com/` → la vitrine ; code source (Ctrl+U) sans `noindex` ;
   - `https://www.al-fissah.com/`, `https://al-fissah.fr/` → renvoient vers `https://al-fissah.com/` ;
   - `https://al-fissah.com/fr/login` → espace étudiant ; `/fr/tarifs`, `/fr/pages/faq` → pages de la vitrine ;
   - `https://al-fissah.com/robots.txt` → `Allow: /` et `Sitemap: https://al-fissah.com/sitemap.xml` ;
   - `https://al-fissah.blackirys.com/robots.txt` → toujours `Disallow: /`.
7. **Google Search Console** : propriété `al-fissah.com` → soumettre
   `https://al-fissah.com/sitemap.xml`, « Inspection de l'URL » → « Demander une indexation ».
8. Plus tard (sans urgence) : sur le serveur OVH, retirer le site Laravel d'al-fissah.com en
   gardant blog et livres ; garder une sauvegarde de la base.

Revenir en arrière : remettre `193.70.85.109` (A) et `2001:41d0:302:2200::59c5` (AAAA) sur `@` et `www`.

## (Historique) Samedi 21/11 — ouvrir à Google

Jusqu'au samedi 21/11/2026, `preview=oui` dans `site.conf` : **les deux adresses**
(al-fissah.fr et al-fissah.blackirys.com) demandent à Google de ne pas les indexer
(`noindex` dans chaque page + `robots.txt` = `Disallow: /`). C'est voulu.

Le jour J, dans cet ordre :

1. **Une seule fois, avant tout** (si ce n'est pas déjà fait) : sur GitHub, dépôt
   `al-fissah-site` → *Settings* → *Secrets and variables* → *Actions* → onglet
   **Variables** → *New repository variable* : nom `FTP_DOSSIER_FR`, valeur = le dossier
   d'al-fissah.fr vu depuis le compte FTP (celui où se trouve aujourd'hui son `index.html`,
   à relever dans FileZilla — par exemple `/al-fissah.fr/`, **avec** les barres `/` au début
   et à la fin). Si al-fissah.fr est sur un autre compte FTP que blackirys, ajouter aussi les
   secrets `FTP_HOST_FR`, `FTP_USERNAME_FR`, `FTP_PASSWORD_FR`.
   Tant que cette variable est vide, la mise en ligne n'envoie **rien** vers al-fissah.fr.
2. Dans `site.conf` : remplacer `preview=oui` par **`preview=non`** (ne rien toucher d'autre :
   `site=https://al-fissah.fr` reste tel quel).
3. Enregistrer sur `main` (modification directe sur GitHub ou fusion d'une demande de
   fusion). La mise en ligne automatique repart seule et :
   - construit **al-fissah.fr** avec `preview=non` → pages indexables, `robots.txt` =
     `Allow: /` + `Sitemap: https://al-fissah.fr/sitemap.xml` ;
   - construit **al-fissah.blackirys.com** avec `--preview` → **toujours** `noindex` et
     `robots.txt` bloquant (le workflow refuse d'envoyer s'il ne l'est pas) ; ses balises
     canoniques désignent al-fissah.fr.
4. Contrôler une fois l'action terminée (onglet *Actions*, coche verte) :
   - `https://al-fissah.fr/robots.txt` → `Allow: /` et la ligne `Sitemap:` ;
   - `https://al-fissah.blackirys.com/robots.txt` → `Disallow: /` ;
   - code source de `https://al-fissah.fr/` (Ctrl+U) : **pas** de `noindex` ;
   - `https://www.al-fissah.fr/` → redirige vers `https://al-fissah.fr/` ;
   - `https://al-fissah.fr/fr/login` → redirige vers l'espace étudiant.
5. **Google Search Console** : ajouter la propriété `al-fissah.fr`, soumettre
   `https://al-fissah.fr/sitemap.xml`, puis « Inspection de l'URL » → « Demander une
   indexation » pour l'accueil.

Revenir en arrière : remettre `preview=oui` et enregistrer sur `main`.

Les boutons Google Play / App Store de l'accueil restent masqués tant que
`appli_publiee=non` (même fichier) : passer à `oui` le jour où les deux fiches des
boutiques sont publiques.

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
