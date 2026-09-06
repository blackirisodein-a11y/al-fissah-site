# Site Al-Fissah — guide de mise en ligne

Textes repris de al-fissah.com (accueil, à propos, programmes, tarifs, FAQ, règlement intérieur, contact).

## Pages
| Fichier | Contenu |
|---|---|
| `index.html` | Accueil : hero, parcours, 3 piliers (programme / immersion / suivi), 6 programmes, vidéo YouTube, adultes, application, tarifs (extrait), témoignages, FAQ (extrait), **formulaire de cours d'essai** |
| `programmes.html` | Fiches détaillées : arabe enfants, arabe adultes, Coran, Mutûn (5 niveaux), méthode de lecture, cours collectifs |
| `tarifs.html` | Grille complète arabe + Coran (formules 1 à 7, binôme), réduction famille, paiement |
| `faq.html` | FAQ officielle complète (18 questions) |
| `reglement.html` | Règlement intérieur officiel (9 articles) |
| `a-propos.html` | Présentation de l'institut, « Al-Fissah c'est… », Coran, liens blog |
| `temoignages.html` | Les 24 témoignages réels (2021–2025), avec données structurées « avis » pour Google |
| `contact.html` | Formulaire Nom / Prénom / E-mail / Sujet / Message + infos pratiques |
| `mentions-legales.html` | Mentions légales, CGV, confidentialité (à compléter : parties entre crochets) |
| `assets/style.css`, `assets/main.js` | Styles et scripts communs |

Site 100 % statique : déposez le dossier tel quel sur n'importe quel hébergeur.

## Formulaires (cours d'essai + contact) — à régler dans `assets/main.js`
```js
const FORM_ENDPOINT="";                       // ex. "https://formspree.io/f/xxxxxxxx"
const CONTACT_EMAIL="c.alfissah@gmail.com";   // adresse qui reçoit les demandes
const WHATSAPP_NUMBER="";                     // ex. "33612345678" — affiche un lien WhatsApp
```
- Sans endpoint : le formulaire ouvre la messagerie du visiteur avec un e-mail pré-rempli.
- Avec endpoint (Formspree, Web3Forms, Getform…) : envoi direct + confirmation à l'écran.

## À vérifier avant la mise en ligne
1. **Adresse e-mail** : `c.alfissah@gmail.com` (confirmée) — présente dans `main.js`, les pages Contact et les mentions légales.
2. **Témoignages** : les 24 avis réels du site sont intégrés (page `temoignages.html` + 3 extraits sur l'accueil).
3. **Vidéo** : l'accueil intègre la vidéo YouTube « Livre 12 Unité 11 » ; changez l'ID dans `build.py` ou `index.html`.
4. **Mentions légales** : rédigées pour **Al-Fissah LLC** (Nouveau-Mexique, USA). Restent à compléter : adresse du siège, NM Business ID, agent enregistré, directeur de publication, hébergeur.
5. **Boutons « Choisir »** des tarifs : pointent vers le formulaire d'essai ; pour renvoyer vers la commande en ligne, mettez les liens `al-fissah.com/fr/commander/...`.
6. « Se connecter » → `https://al-fissah.com/fr/login`.

## Regénérer les pages
`python3 build.py` (header/footer/textes communs dans ce fichier). Les fichiers HTML peuvent aussi être édités directement.
