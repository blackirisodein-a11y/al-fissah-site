# Reprendre ce projet avec Claude Code

## 1. Installer Claude Code (une seule fois)

Ouvrez l'invite de commandes Windows (touche Windows, tapez `cmd`, Entrée) :

```
npm install -g @anthropic-ai/claude-code
```

Si `npm` n'est pas reconnu, installez d'abord Node.js depuis nodejs.org
(version LTS, cochez « Add to PATH »), puis relancez la commande.

Claude Code existe aussi dans l'application de bureau Claude, onglet « Code » :
c'est plus simple si vous préférez éviter l'invite de commandes.

## 2. Ouvrir le projet

Dézippez le dossier `site` quelque part de stable, par exemple
`D:\Projet Al-fissah\site`. Puis :

```
cd "D:\Projet Al-fissah\site"
claude
```

Claude Code démarre dans ce dossier et voit tous les fichiers.

## 3. Premier message à lui envoyer

Copiez-collez ceci :

> Lis CLAUDE.md, c'est la note de reprise du projet. Puis fais le point sur
> l'état du site et dis-moi ce qui reste à faire.

Le fichier `CLAUDE.md` contient tout : l'architecture, la commande de build,
les décisions prises, les pièges de déploiement et la suite prévue.
Claude Code le lit automatiquement à chaque session.

## 4. Ce qui change pour vous

- Il modifie les fichiers directement : plus de zips à télécharger.
- Il lance `python3 build.py --inline` lui-même et régénère les 72 pages.
- Il peut vérifier le rendu et corriger avant de vous montrer le résultat.
- Le transfert FTP reste à votre charge — Claude Code n'a pas vos identifiants.

## 5. Ce qu'il faut lui redire au besoin

- Toujours construire avec `--inline` (voir CLAUDE.md pour la raison).
- Ne pas modifier les `.html` à la main : ils sont générés depuis `lang/*.py`.
- Ne pas téléverser `build.py`, `lang/`, `site.conf` ni les `.md`.
