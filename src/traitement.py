import contextlib
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


def file_regroup(directory):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            dir_type = os.path.join(directory, os.path.splitext(file)[-1].replace('.', ''))
            with contextlib.suppress(FileExistsError):
                os.mkdir(dir_type)
            yield f'👌{shutil.move(os.path.join(directory, file) , dir_type)}' + '\n'


def file_refactor(directory, filetype, destination, move_mode):
    """
    Vérifie si un fichier du dossier directory se termine avec l'extension
    donnée en filetype et le copie si c'est le cas vers le dossier destination.
    À la fin il renvoie une liste de tous les fichiers copiés pour notifier
    l'utilisateur
    :param move_mode: Copie simple ou déplacement
    :param directory : Dossier de départ des fichiers
    :param filetype : Extension des fichiers
    :param destination : Dossier de destination
    :return : Liste contenant les adresses des fichiers copiée
    """
    destination = os.path.abspath(destination)
    # Si le dossier n'existe pas on le crée
    fun = shutil.copy if move_mode == 'Copie' else shutil.move
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
                    yield f'👌{fun(path_file, destination)}' + '\n'
