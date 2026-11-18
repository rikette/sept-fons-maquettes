"""Prépare Sept-Fons-maquettes.zip à envoyer aux frères (page de choix, 8 versions, assets, mode d'emploi)."""
import os, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Sept-Fons-maquettes.zip")
TOP = "Sept-Fons-maquettes"

LISEZ_MOI = """MAQUETTES DU SITE DE L'ABBAYE DE SEPT-FONS
==========================================

1. Dézippez ce dossier (clic droit > « Extraire tout… »).
2. Ouvrez le fichier index.html avec Google Chrome ou Microsoft Edge
   (clic droit > « Ouvrir avec »). Une connexion Internet est utile pour les polices.
3. Cliquez sur une version : elle s'ouvre dans un nouvel onglet.

DONNER SON AVIS
- En bas à droite, cliquez sur « ✎ Commenter ».
- À la première ouverture, le site vous demande votre prénom (pour signer vos remarques).
- Cliquez sur n'importe quel élément (titre, photo, menu, bouton…) et choisissez
  👍 J'aime ou 👎 Je n'aime pas. Vous pouvez écrire une remarque.
- Le lien « ↥ Le bloc entier » permet de commenter toute la section.
- Le bouton ◉ masque ou affiche vos remarques. Le bouton ☰ les liste toutes.
- Cliquez sur « ✓ Terminer » pour naviguer normalement de nouveau.

Vos remarques restent dans votre navigateur, même si vous fermez la page.
Utilisez toujours le même navigateur, et n'effacez pas l'historique avant l'envoi.

RENVOYER SES REMARQUES
- Cliquez sur ☰ puis « Envoyer les remarques ».
- Un fichier « remarques-votre-prenom-date.json » est enregistré dans vos Téléchargements.
- Joignez ce fichier à un courriel et renvoyez-le.

FAIRE PASSER LES REMARQUES DE FRÈRE EN FRÈRE
- Le frère qui reçoit le fichier ouvre le site, clique sur ☰ puis
  « Ouvrir un fichier de remarques reçu… » et choisit ce fichier.
- Il voit alors les remarques des autres (pastilles en pointillés, signées),
  ajoute les siennes, puis « Envoyer les remarques » : le nouveau fichier
  contient les remarques de tous. Il le transmet au suivant.

Merci !
"""


def main():
    keep = ["index.html", "assets"] + sorted(d for d in os.listdir(ROOT) if d[:1].isdigit() and os.path.isdir(os.path.join(ROOT, d)))
    n = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{TOP}/LISEZ-MOI.txt", LISEZ_MOI.replace("\n", "\r\n"))
        for k in keep:
            p = os.path.join(ROOT, k)
            if os.path.isfile(p):
                z.write(p, f"{TOP}/{k}"); n += 1; continue
            for base, _, files in os.walk(p):
                for f in files:
                    full = os.path.join(base, f)
                    z.write(full, f"{TOP}/" + os.path.relpath(full, ROOT).replace(os.sep, "/")); n += 1
    print(f"{n} fichiers -> {OUT} ({os.path.getsize(OUT) / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
