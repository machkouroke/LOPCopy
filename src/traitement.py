import os
import re
import shutil


def format_validator(string):
    """
    Vérifie si le format entré est valide
    :param string : format
    :return : Retourne si le format est valide ou non
    """
    return bool(re.match('^[a-zA-Z0-9]+$', string))


def file_refactor(directory, filetype, destination):
    """
    Vérifie si un fichier du dossier directory se termine avec l'extension
    donnée en filetype et le copie si c'est le cas vers le dossier destination.
    À la fin il renvoie une liste de tous les fichiers copiés pour notifier
    l'utilisateur
    :param directory : Dossier de départ des fichiers
    :param filetype : Extension des fichiers
    :param destination : Dossier de destination
    :return : Liste contenant les adresses des fichiers copiée
    """
    destination = os.path.abspath(destination)
    # Si le dossier n'existe pas on le crée
    if not os.path.exists(destination):
        os.mkdir(destination)
    for x, y, z in os.walk(directory):
        # Pour éviter que le script ne parcoure le dossier de destination
        if os.path.abspath(x) != os.path.abspath(destination):
            for k in z:
                if k.endswith(filetype):
                    # Chemin du fichier actuel
                    path_file = os.path.join(directory, x, k)
                    # Copie du fichier
                    yield '👌' + shutil.copy(path_file, destination) + '\n'
