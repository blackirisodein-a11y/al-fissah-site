# Publier sur votre hébergement LWS

Vous avez un hébergement LWS avec un autre nom de domaine que `al-fissah.com`.
C'est la situation idéale : vous publiez le site sur ce domaine, vous le regardez
tranquillement en conditions réelles, et le site actuel d'Al-Fissah continue de
tourner sans être touché.

---

## Étape 1 — Indiquer l'adresse de publication

Ouvrez le fichier **`site.conf`** et remplacez l'adresse par votre domaine LWS :

```
site=https://votre-domaine.fr
preview=oui
```

`preview=oui` ajoute une consigne demandant à Google de ne pas référencer ce site.
C'est important : sans cela, Google risquerait d'afficher votre domaine de test à la
place d'al-fissah.com dans les résultats de recherche, et de considérer les deux comme
du contenu dupliqué. Vous repasserez sur `preview=non` le jour de la bascule
définitive.

Puis, dans le dossier du site :

```
python3 build.py
```

Les 50 pages sont régénérées avec la bonne adresse.

---

## Étape 2 — Récupérer vos accès FTP chez LWS

1. Connectez-vous sur **panel.lws.fr**.
2. Menu **Hébergement** → votre hébergement → onglet **FTP** (ou « Comptes FTP »).
3. Notez : **serveur** (`ftp.votre-domaine.fr`), **identifiant**, **mot de passe**.
   Si vous avez oublié le mot de passe, LWS permet de le réinitialiser ici même.

---

## Étape 3 — Envoyer les fichiers

Téléchargez **FileZilla** (gratuit, filezilla-project.org), puis :

1. En haut de FileZilla : *Hôte* = `ftp.votre-domaine.fr`, *Identifiant*,
   *Mot de passe*, *Port* vide → **Connexion rapide**.
2. À droite (le serveur), entrez dans le dossier public. Chez LWS il s'appelle
   généralement **`public_html`**, parfois **`www`**. Vous devez y voir un
   `index.html` d'accueil LWS ou un dossier vide.
3. À gauche (votre ordinateur), ouvrez le dossier `site`.
4. **Sélectionnez le contenu du dossier, pas le dossier lui-même** — c'est l'erreur
   la plus fréquente. Envoyez :

   ```
   index.html   programmes.html   tarifs.html   faq.html   temoignages.html
   reglement.html   a-propos.html   contact.html   mentions-legales.html
   404.html   sitemap.xml   robots.txt   .htaccess
   assets/   ar/   en/   es/   de/
   ```

5. Glissez-les vers la droite. Comptez une à deux minutes.

> **Fichiers cachés.** Le `.htaccess` commence par un point : FileZilla peut le
> masquer. Menu *Serveur* → cochez **« Forcer l'affichage des fichiers cachés »**.
> Ce fichier est important : il gère le HTTPS, la page 404 et la compression.

### Ne pas envoyer

Ces fichiers servent à fabriquer le site, pas à le faire tourner :

```
build.py   lang/   pics.json   part_classroom.html   site.conf
README.md   MISE-EN-LIGNE.md   LWS.md   CONSULTER-EN-LOCAL.md
netlify.toml   _redirects   demarrer-windows.bat   demarrer-mac-linux.command
```

Gardez-les sur votre ordinateur : sans eux, plus moyen de régénérer les 5 langues.

---

## Étape 4 — Activer le HTTPS

Dans le panel LWS : **Hébergement** → **SSL / Certificat**. Activez le certificat
gratuit Let's Encrypt s'il ne l'est pas déjà. Comptez quelques minutes.

Tant que le certificat n'est pas actif, laissez de côté la redirection HTTPS du
`.htaccess` : si vous voyez une erreur de boucle de redirection, ouvrez le fichier
et mettez un `#` devant les quatre lignes du bloc `RewriteEngine`, le temps que le
certificat soit installé.

---

## Étape 5 — Vérifier

Ouvrez `https://votre-domaine.fr` et contrôlez :

- [ ] la page d'accueil s'affiche avec les animations ;
- [ ] le sélecteur de langue mène bien à `/ar/`, `/en/`, `/es/`, `/de/` ;
- [ ] la version arabe s'affiche de droite à gauche ;
- [ ] une adresse inventée (`/nimportequoi`) affiche bien la page 404 ;
- [ ] le formulaire d'essai ouvre un e-mail vers `c.alfissah@gmail.com` ;
- [ ] le site s'affiche correctement sur votre téléphone.

---

## Mettre à jour plus tard

1. Modifiez le texte dans `lang/fr.py` (ou la langue voulue).
2. `python3 build.py`
3. Renvoyez par FTP les fichiers modifiés — ou tout le contenu, cela écrase l'ancien.

---

## Le jour de la bascule vers al-fissah.com

À ce moment-là seulement :

1. Dans `site.conf` : `site=https://al-fissah.com` et `preview=non`, puis
   `python3 build.py`.
2. **Attention aux liens de l'application** : `/fr/login`, `/fr/register` et les pages
   de commande doivent continuer de pointer vers l'application existante. Si le site
   de présentation prend la racine du domaine, il faut décider avec la personne qui
   gère l'application comment les deux cohabitent (souvent : présentation à la racine,
   application sur un sous-domaine du type `app.al-fissah.com`).
3. Déclarez le site dans **Google Search Console** et soumettez-y `sitemap.xml`.
