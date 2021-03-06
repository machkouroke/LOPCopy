import traitement

from annexe import Warning, helper

# PyQt import
from PyQt6 import uic
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal
from PyQt6.QtWidgets import QFileDialog


class TreatmentSignal(QObject):
    """
    Signal envoyé par la
    la copie
    """
    finished = pyqtSignal(list)
    display = pyqtSignal(str)


class Runner(QRunnable):
    """
    Processsus permettant d'exécuter en parallèle la copie du fichier
    et le lancement du programme
    """

    def __init__(self, directory, filetype, destination, move, recherche):
        super().__init__()
        self.signals = TreatmentSignal()
        self.directory = directory
        self.filetype = filetype
        self.destination = destination
        self.move = move
        self.recherche = recherche

    def run(self):
        answer = traitement.file_refactor(self.directory, self.filetype, self.destination, self.move) \
            if self.recherche != "Intelligent" else traitement.file_regroup(self.directory)
        file_moved = []
        for y in answer:
            self.signals.display.emit(y)
            file_moved.append(y)
        if not file_moved:
            file_moved.append("Aucun fichier ne remplissais les critères demandées")
        else:
            file_moved.insert(0, f'Bravo les fichiers suivants on été déplacé vers "{self.destination}"\n')
        self.signals.finished.emit(file_moved)


class Main:
    def __init__(self, filename):
        # Chargement de la fenêtre et de la fenêtre d'aide à partir de la feuille ui de Qt Designer
        self.windows = uic.loadUi(filename, None)
        self.aide = helper.Helper()
        self.form, self.dep, self.destination = None, None, None
        self.move = 'Copie'
        self.recherche = "Surfacique"
        # Chef d'orchestre des thread
        self.thread = QThreadPool()
        self.windows.progression.hide()
        # Connection slot/signal
        self.windows.personnalise.clicked.connect(self.disable_suggestion)
        self.windows.help_.clicked.connect(self.aide.windows.open)
        self.windows.suggestion.clicked.connect(self.disable_input)
        self.windows.fileType.buttonClicked.connect(self.radio_manager)
        self.windows.moveMode.buttonClicked.connect(self.move_mode)
        self.windows.rechercheType.buttonClicked.connect(self.recherche_type)
        self.windows.select_dep.clicked.connect(self.select_dep_directory)
        self.windows.select_end.clicked.connect(self.select_destination_directory)
        self.windows.demarrer.clicked.connect(self.processing)

        # Ouverture de la fenêtre
        self.windows.show()

    def recherche_type(self, i):
        self.recherche = i.text()
        if self.recherche == "Intelligent":
            for j in {self.windows.extension, self.windows.dest_path, self.windows.select_end,
                      self.windows.copie, self.windows.deplacement}:
                j.setEnabled(False)
            return
        for j in {self.windows.extension, self.windows.dest_path, self.windows.select_end, self.windows.copie_move,
                  self.windows.copie, self.windows.deplacement}:
            j.setEnabled(True)

    def move_mode(self, i):
        self.move = i.text()

    def radio_manager(self, i):
        self.form = i.text().lower()

    # Les deux fonctions suivantes empêchent les options 'Suggestion' et 'Personnalise' d'etre
    # activé à la fois
    def disable_suggestion(self):
        self.windows.suggestion.setChecked(False)

    def disable_input(self):
        self.windows.personnalise.setChecked(False)

    def select_dep_directory(self):
        """
        Slot permettant de gérer la sélection du répertoire de départ par
        l'ouverture d'une boite de dialogue
        """
        file_name = QFileDialog.getExistingDirectory()
        self.windows.dep_path.setText(file_name)

    def select_destination_directory(self):
        """
        Slot permettant de gérer la sélection du répertoire de départ par
        l'ouverture d'une boite de dialogue
        """
        file_name = QFileDialog.getExistingDirectory()
        self.windows.dest_path.setText(file_name)

    def finished(self, ans):
        self.windows.progression.hide()
        self.windows.log.setText('\n'.join(ans))

    def processing(self):
        """
        Cette fonction effectue le traitement demandé par l'utilisateur tout en
        vérifiant qu'il n'ait pas fait d'erreur
        """
        # Path de depart et de destination
        self.dep = self.windows.dep_path.text()
        self.destination = self.windows.dest_path.text() if self.recherche != 'Intelligent' else self.dep

        # Vérifie que tous les champs ont bien été saisi
        if self.recherche != "Intelligent":
            if self.windows.personnalise.isChecked():
                if not self.windows.format.text():
                    Warning.Dialog("Veuillez entrer un format")
                    return
                elif traitement.format_validator(self.windows.format.text()):
                    # Format choisi
                    self.form = self.windows.format.text().lower()
                else:
                    Warning.Dialog("Format non valide veuillez réessayer")
                    return
            elif not (self.windows.suggestion.isChecked() or self.windows.personnalise.isChecked()):
                Warning.Dialog("Veuillez sélectionner un Format pour que je puisse vous aider !!")
                return
            if self.form is None:
                Warning.Dialog("Veuillez sélectionner un Format pour que je puisse vous aider!!")
                return
            if not self.destination:
                Warning.Dialog("Le chemin de destination n'a pas été saisi")
                return
        if not self.dep:
            Warning.Dialog("Le chemin de départ n'a pas été saisi")
            return

        self.windows.progression.show()
        process = Runner(self.dep, self.form, self.destination, self.move, self.recherche)
        process.signals.display.connect(self.windows.log.setText)
        process.signals.finished.connect(self.finished)
        self.thread.start(process)
