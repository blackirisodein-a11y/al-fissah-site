# Al-Fissah — note de reprise

Site vitrine statique de l'**École internationale de langue arabe et Coran** (Al-Fissah LLC,
Nouveau-Mexique, USA). 6 langues, 12 pages par langue, aucun serveur applicatif.

En ligne (préproduction) : **https://al-fissah.blackirys.com** — hébergement LWS, dépôt par FTP.
Destination finale : al-fissah.com (le domaine héberge déjà l'application élève : `/fr/login`,
`/fr/register`, paiements Stripe — **ne pas écraser**).

---

## Comment ça marche

Les fichiers `.html` sont **générés**, jamais édités à la main. Tout part de :

```
build.py              assemble les pages ; contient la structure HTML et le dict PARCOURS
lang/fr.py            tous les textes français (dict L)
lang/{en,es,de,ru,ar}.py   mêmes clés, autres langues
lang/testimonials.py  les 24 témoignages réels (restent en français partout)
assets/style.css      styles
assets/main.js        scripts (loader, menu, formulaires, sélecteur de langue)
assets/logo*.png      logo officiel
site.conf             adresse de publication + mode aperçu
pics.json             illustrations SVG des 6 programmes (extraites du template d'origine)
part_classroom.html   bloc "classe virtuelle" du hero
```

### Construire

```bash
python3 build.py --inline        # ← MODE UTILISÉ EN PRODUCTION
python3 build.py                 # version avec assets externes (non déployée)
python3 build.py fr en           # seulement certaines langues
python3 build.py --site https://exemple.fr --preview
```

**`--inline` est important.** Il intègre CSS, JS et logos (base64) dans chaque page.
Raison : les transferts FTP par FileZilla créaient le dossier `assets` sans y déposer les
fichiers, ce qui cassait tout le site en silence. Avec `--inline`, chaque page est autonome ;
si une page manque au transfert, elle seule est concernée. Pages ~300 Ko, ~11 Mo au total.

### Vérifier

Playwright est installé. Le contrôle systématique après chaque build :

```js
// 72 pages : erreurs JS, débordement horizontal, logo chargé
for (const l of ['','ar/','en/','es/','de/','ru/'])
  for (const f of ['index','programmes','tarifs','faq','temoignages','reglement',
                   'a-propos','contact','essai','inscription','mentions-legales','404'])
    // goto → forcer loader.done + body.ready → scrollWidth <= viewport, pageerror vide
```

Le débordement horizontal est le défaut qui revient le plus (arabe RTL, textes allemands longs).

---

## Décisions à connaître

- **`site.conf`** : `site=` alimente les balises canoniques et le sitemap ; `preview=oui`
  ajoute `noindex` + `robots.txt` bloquant. À passer sur `non` uniquement le jour de la
  bascule vers al-fissah.com, sinon le domaine de test concurrence le vrai site.
- **Deux parcours distincts, à ne pas confondre** :
  - « Commencer maintenant » → `inscription.html` = **inscription aux études** (programme,
    formule, professeur, créneaux, paiement)
  - « Demander un essai gratuit » (bouton en haut à droite) → `essai.html` = **cours d'essai**
    30 min, gratuit, sans engagement
  Les libellés et textes des deux pages sont dans le dict `PARCOURS` de `build.py`.
  **Boutons** (demande du client) : en-tête, « Demander un essai gratuit » **orange** ; hero,
  « Commencer maintenant » orange mis en avant (`.btn-hero`) + « Voir le programme » (`home.cta2`,
  contour bleu marine) — le bouton d'essai n'est plus dans le hero. Ailleurs (menu mobile,
  contact) le bouton d'essai est bleu marine.
  L'en-tête porte le libellé complet ; pour qu'il tienne, le menu de bureau n'a pas « Accueil »
  (le logo y mène), le menu passe en « hamburger » sous 1180 px, et sous 560 px le bouton affiche
  le libellé court (`btn_essai_court`). Contrôle : mesurer logo / menu / bloc droit à
  1440-1366-1280-1181-1180-1000-800-700-641-640-480-390 px dans les 6 langues.
- **Chaque page a son propre formulaire**, distinct de l'autre :
  - `essai.html` → `#trial-form` (profil, programme, niveau, coordonnées, disponibilités) ;
    textes dans `lang/*.py` dict `'form'`.
  - `inscription.html` → `#signup-form` (élève, programme, niveau, **formule 1–7 h / binôme /
    collectif**, jours souhaités, début souhaité, coordonnées, acceptation du règlement) ;
    textes dans `lang/*.py` dict `'signup'` (en fin de fichier) + messages `L['js']`.
  - Les deux passent par le même mécanisme que le contact (`assets/main.js` : Web3Forms si
    `FORM_ENDPOINT` est rempli, sinon e-mail pré-rempli). Le champ `_type` vaut
    `inscription` pour l'inscription, ce qui permet de trier les demandes reçues.
  - Les boutons « Choisir » des tarifs et les CTA des programmes préremplissent le
    formulaire d'inscription (`inscription.html?formule=2&programme=coran`).
  - Sous le formulaire, les 6 étapes du parcours cible restent décrites (`PARCOURS`,
    `steps`), avec une note (`steps_p`) précisant que l'administration réalise pour l'instant
    les étapes 3 à 5 à la main. Le parcours réel viendra d'une plateforme existante (voir
    « suite » plus bas).
- **Textes** : repris de al-fissah.com (FAQ 18 questions, règlement 9 articles, tarifs,
  programmes). Ne pas les réécrire sans raison, ce sont les textes officiels de l'école.
- **Témoignages** : verbatim, en français dans les 6 langues. Une note l'explique sur les
  versions traduites. Ne pas traduire sans accord du client.
- **Mentions légales** : rédigées pour une LLC américaine servant des élèves européens
  (droit du Nouveau-Mexique + RGPD + transferts hors UE). Cinq champs restent entre
  crochets : adresse du siège, NM Business ID, agent enregistré, gérant, hébergeur.
- **Formulaires (contact, essai, inscription)** : `assets/main.js`, en haut. `FORM_ENDPOINT` vide → ouvre la
  messagerie du visiteur vers `c.alfissah@gmail.com`. Renseigner `FORM_ENDPOINT` +
  `FORM_KEY` (Web3Forms) pour recevoir les demandes directement.
- **Dépôt GitHub** : `blackirisodein-a11y/al-fissah-site` contient tout le dossier `site` (y compris
  `build.py`, `lang/`, `assets/`) — Netlify en a besoin pour reconstruire. La règle « ne pas
  téléverser » ne concerne que le FTP vers LWS.
- **`ASSET_VER`** dans `build.py` : numéro de version sur `style.css`/`main.js` en mode non
  inline, pour contourner le cache navigateur. Sans effet en mode `--inline`.
- **Écran d'ouverture** (accueil seulement) : fond **clair** et vivant (dégradé blanc → bleu pâle
  → pêche qui glisse, halos orange et bleu qui dérivent, trame de points, lettres arabes
  `LD_SYMS` qui montent lentement — demande du client : « fond plus clair avec des animations »),
  logo qui arrive en douceur avec une onde lumineuse, titre tapé (`js.typew`, ≈ 85 ms/lettre) puis sous-titre en fondu
  (`js.typew_sub`) et trait orange qui se remplit ; sortie en rideau vers le haut. ≈ 5 s au
  total — rythme voulu par le client, ne pas accélérer. Il ne s'affiche qu'à la **première entrée de la session** : `sessionStorage`
  `af-intro` + classe `html.intro-seen` posée par un script inline dans le `<head>` (évite tout
  flash au clic sur le logo). Filet de sécurité CSS (`@keyframes ldfailsafe`) : il s'efface au
  bout de 7 s même si le JS ne se charge pas. Ne pas le retirer — sans lui, un JS absent
  bloquait tout le site derrière l'écran bleu.

---

## Déploiement

**Automatique depuis GitHub** (`.github/workflows/mise-en-ligne.yml`) : chaque push sur `main`
reconstruit les pages (`--inline`) et les envoie par FTP dans `/al-fissah.blackirys.com`.
Les identifiants sont des secrets du dépôt (`FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD`),
jamais dans le code ni dans la conversation. Suivi : onglet *Actions* du dépôt ; on peut y
relancer l'envoi à la main (*Run workflow*). Le poste du client n'a plus besoin de FileZilla.

Méthode manuelle de secours — FTP (FileZilla), hôte `193.37.145.67`, **FTP simple sans chiffrement** — le TLS échoue,
le certificat LWS ne correspond pas au domaine. Déposer le contenu (pas le dossier) dans
`/al-fissah.blackirys.com`.

**Piège vérifié plusieurs fois** : FileZilla crée les dossiers mais n'y copie pas toujours
les fichiers. Toujours contrôler ensuite qu'une ressource répond, p. ex. ouvrir
`al-fissah.blackirys.com/ru/` dans un navigateur. La formule LWS du client ne donne accès
ni au gestionnaire de fichiers ni à PHP.

Ne jamais téléverser : `build.py`, `lang/`, `site.conf`, `pics.json`, `part_classroom.html`,
les `.md`, `netlify.toml`, `_redirects`.

---

## Plateforme des comptes (dépôt `blackirisodein-a11y/al-fissah-app`)

Décision du client (09/2026) : **ce site reste la vitrine, tel quel.** La plateforme
(adaptée de celle d'une autre école : Next.js + Supabase) ne sert qu'aux **comptes** :
inscription aux études (`/fr/inscription`), demande d'essai gratuit (`/fr/essai`),
connexion et espace élève (`/fr/login`), espace bureau. Ses anciennes pages vitrine
renvoient vers ce site.

Le branchement se fait par **une seule ligne de `site.conf`** : `app=` (adresse de la
plateforme, sans barre finale). Tant qu'elle est vide, rien ne change. Une fois renseignée
et le site reconstruit :
- « Se connecter » / « S'inscrire » (en-tête, menu mobile, pied de page) → `{app}/{langue}/login`
  et `/register` ;
- **« Demander un essai gratuit » et « Commencer maintenant » mènent directement à la
  plateforme** (`{app}/{langue}/essai` et `/inscription`) — demande du client (09/2026) :
  aucune page intermédiaire « S'inscrire aux études » entre le site et la plateforme.
  Idem pour les boutons « Choisir » des tarifs et les CTA des programmes (paramètres
  `?formule=…&programme=…` conservés) et pour tous les liens « essai » du site
  (`essai_url()` / `insc_url()` dans `build.py`).
- `essai.html` et `inscription.html` ne sont plus que des pages de renvoi immédiat
  (`meta refresh` + `location.replace`, `noindex`, hors sitemap) pour les anciens liens ;
  leur formulaire local et l'encart `.app-card` ne servent que si `app=` est vide.
- les pages es/de renvoient vers la version anglaise de la plateforme (elle n'existe qu'en
  fr/en/ar/ru).
Contrôle : `grep -o 'href="https://[^"]*/fr/\(essai\|inscription\)[^"]*"' index.html tarifs.html`.

**Cours d'essai : validation du bureau (09/2026).** Sur la plateforme, la demande d'essai
n'est plus acceptée d'office : l'élève choisit une demi-heure, sa demande arrive « en
attente » et il voit un message le disant. Le bureau accepte ou refuse depuis
« Demandes d'essai » ; l'acceptation crée seule le compte, le cours et l'e-mail
d'identifiants. Rien ne part avant. Détail dans `ADAPTATION-AL-FISSAH.md` du dépôt de
la plateforme.

## Suite prévue

1. Plateforme en service sur **https://al-fissah-app-nine.vercel.app** (Supabase + Vercel,
   06/09/2026) et `app=` renseigné : le site y envoie déjà. Son habillage a été refondu
   (09/2026) sur l'identité de ce site : palette marine / orange, Space Grotesk + Karla,
   cartes 20 px, en-têtes à kicker orange ; règles dans `docs/SYSTEME-GRAPHIQUE.md` du
   dépôt de la plateforme, contrôle par le workflow « Capturer les pages » (branche
   `captures`). Restent : e-mails (Resend, en place, à tester), paiements (Stripe), puis
   domaine définitif (app.al-fissah.com) → mettre à jour `app=`.
2. Compléter les mentions légales.
3. Brancher le formulaire de contact sur Web3Forms.
4. Basculer vers al-fissah.com en préservant les URL de l'application élève.

## Style de travail attendu

Le client n'est pas technicien : instructions pas à pas, une action à la fois, pas de jargon.
Il travaille sous Windows avec FileZilla. Vérifier soi-même le rendu (captures Playwright)
avant d'annoncer que quelque chose fonctionne — plusieurs allers-retours ont été perdus à
supposer qu'un transfert avait réussi.
