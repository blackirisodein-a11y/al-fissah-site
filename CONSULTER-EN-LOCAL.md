# Consulter le site en local

## Le plus simple
Double-cliquez sur **`index.html`**. Le site s'ouvre dans votre navigateur et tout
fonctionne : navigation, langues, animations, accordéons, formulaires.

## Avec un petit serveur local (recommandé)
Certaines choses ne se comportent pas exactement comme sur un vrai hébergement quand
on ouvre un fichier directement (adresses du type `file:///...`). Pour être au plus
près du rendu final :

- **Windows** : double-cliquez sur `demarrer-windows.bat`
- **Mac / Linux** : double-cliquez sur `demarrer-mac-linux.command`

Le site s'ouvre alors sur **http://localhost:8000**. Laissez la fenêtre noire ouverte
tant que vous consultez le site ; fermez-la pour arrêter.

> Ces scripts utilisent Python, déjà installé sur Mac et Linux. Sous Windows, si rien
> ne se passe, installez Python depuis python.org (cochez « Add to PATH ») ou
> contentez-vous du double-clic sur `index.html`.

## Les adresses en local
| Langue | Adresse |
|---|---|
| Français | http://localhost:8000/ |
| العربية | http://localhost:8000/ar/ |
| English | http://localhost:8000/en/ |
| Español | http://localhost:8000/es/ |
| Deutsch | http://localhost:8000/de/ |

## Modifier le contenu
Deux façons de faire :

1. **Rapide** : ouvrez le fichier `.html` concerné dans un éditeur de texte
   (Bloc-notes, TextEdit, VS Code) et modifiez le texte. Attention : une modification
   faite ainsi sera écrasée si vous relancez `build.py`.
2. **Propre** : modifiez le texte dans `lang/fr.py` (ou `ar.py`, `en.py`, `es.py`,
   `de.py`), puis lancez `python3 build.py` dans le dossier. Toutes les pages de
   toutes les langues sont régénérées.

## Le logo
Le fichier affiché est `assets/logo.svg` — un logo provisoire aux couleurs de l'école,
pour que le site fonctionne même sans connexion internet. Pour mettre le vrai logo :
déposez votre fichier dans `assets/` et changez la ligne `LOGO_FILE` en haut de
`build.py`, puis relancez `python3 build.py`.

## Imprimer une page
Le règlement intérieur, les tarifs, la FAQ et les mentions légales sont mis en forme
pour l'impression : Ctrl+P (Cmd+P sur Mac) donne un document propre, sans menu ni
animations, avec les réponses des accordéons dépliées. Pratique pour remettre le
règlement aux parents.

## Ce qui ne marche qu'une fois en ligne
- L'envoi automatique des formulaires (en local, ils ouvrent votre messagerie —
  ce qui est déjà utilisable). Voir `FORM_ENDPOINT` dans `assets/main.js`.
- Les données structurées et le `sitemap.xml`, utiles seulement pour Google.
- Les polices Google Fonts et les vidéos YouTube : sans connexion, le site s'affiche
  avec les polices de votre système. C'est normal et sans conséquence.
- Les mentions légales : les parties entre crochets `[…]` restent à compléter avant
  toute mise en ligne publique.
