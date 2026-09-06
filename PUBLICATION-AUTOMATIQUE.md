# Publication automatique — plus jamais de téléchargement

Aujourd'hui, chaque modification vous oblige à récupérer un fichier puis à l'envoyer
par FTP. Cette installation supprime complètement cette corvée.

**Après la mise en place :** vous modifiez un texte depuis votre navigateur, et une
minute plus tard le site est à jour en ligne, dans les 5 langues. Pas de
téléchargement, pas de FileZilla, pas de Python à installer.

Comptez **15 à 20 minutes**, une seule fois.

---

## Comment ça marche

Vos textes vivent sur **GitHub** (un coffre-fort de fichiers, gratuit). **Netlify**
surveille ce coffre : dès qu'un texte change, il relance `build.py`, régénère les 50
pages et les publie. Vous ne touchez jamais aux fichiers `.html` — ils sont fabriqués
automatiquement à partir des fichiers de langue.

```
Vous modifiez lang/fr.py  →  GitHub  →  Netlify régénère  →  site à jour
        (navigateur)                        (1 minute)
```

---

## Étape 1 — Créer le coffre GitHub (5 min)

1. Créez un compte gratuit sur **github.com** (bouton *Sign up*).
2. Une fois connecté, cliquez sur **+** en haut à droite → **New repository**.
3. *Repository name* : `al-fissah-site`.
   Cochez **Private** si vous ne voulez pas que le contenu soit public.
   Ne cochez rien d'autre. → **Create repository**.
4. Sur la page qui s'affiche, cliquez sur le lien **uploading an existing file**.
5. Ouvrez votre dossier `site` sur l'ordinateur, **sélectionnez tout** (Ctrl+A) et
   glissez-le dans la zone de dépôt de GitHub.
6. En bas, bouton vert **Commit changes**.

Vos fichiers sont en sécurité, avec l'historique de toutes les versions.

## Étape 2 — Brancher Netlify (5 min)

1. Compte gratuit sur **netlify.com** → *Sign up* → **Sign up with GitHub**
   (le plus simple : cela relie les deux comptes d'un coup).
2. **Add new site** → **Import an existing project** → **GitHub**.
3. Autorisez Netlify à lire vos dépôts, puis choisissez **al-fissah-site**.
4. Netlify lit tout seul le fichier `netlify.toml` déjà présent :
   commande `python3 build.py`, dossier `.`. **Ne changez rien.** → **Deploy**.
5. Après une minute, votre site est en ligne sur une adresse du type
   `chose-machin-123.netlify.app`. Cliquez pour vérifier.

> Pour une adresse plus jolie : *Site configuration → Change site name*, par exemple
> `al-fissah`, ce qui donne `al-fissah.netlify.app`.

## Étape 3 — Votre nom de domaine (facultatif, 5 min)

Pour utiliser votre domaine LWS plutôt que l'adresse Netlify :

1. Netlify : *Domain management* → **Add a domain** → saisissez votre domaine.
2. Netlify affiche une valeur à recopier (un enregistrement **CNAME**, ou des
   serveurs de noms).
3. Panel LWS → **Zone DNS** de votre domaine → ajoutez l'enregistrement indiqué.
4. Comptez de 10 minutes à quelques heures. Le certificat HTTPS s'installe seul.

N'oubliez pas de mettre `site.conf` à jour avec cette adresse (voir ci-dessous) :
c'est en une modification, comme n'importe quel texte.

---

## Modifier un texte, désormais

1. Sur GitHub, ouvrez le dossier **`lang`** puis le fichier de la langue :
   `fr.py`, `ar.py`, `en.py`, `es.py` ou `de.py`.
2. Cliquez sur l'icône **crayon** ✏️ en haut à droite.
3. Modifiez le texte entre les guillemets.
4. En bas : **Commit changes**.
5. Une minute plus tard, le site est à jour. Vous pouvez suivre l'avancement dans
   l'onglet *Deploys* de Netlify.

### La seule règle à respecter

Ne touchez **ni aux guillemets, ni aux virgules, ni aux noms devant le signe `=`**.
Modifiez uniquement le texte *à l'intérieur* des guillemets.

```python
tarifs_h2="Des sessions de 4 semaines, à votre rythme",
          └──────────── modifiez seulement ceci ────┘
```

Si vous supprimez un guillemet par mégarde, la reconstruction échoue et **le site en
ligne reste tel qu'il était** — rien n'est cassé. Netlify vous envoie un e-mail, vous
corrigez, et c'est reparti. C'est le filet de sécurité de ce système.

### Où trouver quoi

| Ce que vous voulez changer | Fichier | Repère |
|---|---|---|
| Textes de l'accueil | `lang/fr.py` | section `'home'` |
| Programmes | `lang/fr.py` | section `'progs'` |
| Tarifs | `lang/fr.py` | section `'tarifs'` |
| Questions de la FAQ | `lang/fr.py` | section `'faq'` |
| Règlement intérieur | `lang/fr.py` | section `'reglement'` |
| Mentions légales | `lang/fr.py` | section `'mentions'` |
| Témoignages | `lang/testimonials.py` | communs aux 5 langues |
| Adresse du site | `site.conf` | `site=` et `preview=` |
| Adresse e-mail, formulaires | `assets/main.js` | en haut du fichier |
| Couleurs, mise en page | `assets/style.css` | |
| Logo | `assets/logo.svg` | remplacez le fichier |

---

## Aperçu avant publication

Netlify crée automatiquement un aperçu pour chaque modification proposée. Si vous
préférez vérifier avant de publier :

Sur GitHub, au moment de valider, choisissez **« Create a new branch and start a pull
request »** au lieu de *Commit directly*. Netlify vous donne alors une adresse d'essai
privée. Si le résultat vous plaît, vous fusionnez — et le site public se met à jour.

---

## Et si vous préférez rester sur LWS ?

Ce système fonctionne aussi : Netlify publie, et vous gardez LWS pour vos e-mails ou
d'autres sites. Rien ne vous oblige à choisir. Vous pouvez même tester Netlify
tranquillement et ne basculer votre domaine que si le résultat vous convainc.
