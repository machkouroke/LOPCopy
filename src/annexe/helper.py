from PyQt6 import uic

msg = """Bienvenue dans LOPCopy
LOPCopy vous permet de regrouper rapidement et simplement les fichiers que vous lui demandiez.
Cela peut se faire par les étapes suivantes:
1 - Sélection du type de fichier à copier:
Nous vous donnons la possibilité de saisir votre propre type de fichier (juste le nom 
de l'extension sans le '.') ou juste de choisir l'un des types basiques proposé par LOPCopy
2- Sélection du dossier de départ:
Le dossier de départ est le dossier qui contient les fichiers que vous vouliez copier.
3 - Sélection du dossier de destination:
Ce champ contient le chemin du dossier où LOPCopy doit copier vos fichier. Il est à noter que si ce chemin
n'existe pas il seras automatiquement crée en tant que nouveau dossier.
Vous pouviez suivre l'évolution de votre copie avec la fenêtre de logging situé dans la partie inférieur du programme.
De plus à la fin de la copie il vous affiche le chemin de tous les fichiers copié.
Nous vous remercions pour votre copie.
"""


class Helper:
    def __init__(self):
        self.windows = uic.loadUi('UI/help.ui')
        self.windows.help_msg.setText(msg)
        self.windows.exec()
