'''
    Fichier declarant la structure generique d'un scenario
'''
from typeAnnotations import *
import types

DELAY = 5 # Delai par defaut entre deux tentatives de test pour un etudiant
INFINITE_ATTEMPTS = -1

class Scenario():

    '''
        Classe generique rassemblant les caracteristiques communes a tous les scenario de test. Cette classe possède une variable statique qui permet de récupérer
        toutes les instances de scenario créées.

        Parametres du constructeur:
            _tools : liste de Tool - La liste des outils utilisés dans ce scenario
            _nb_attempts : Entier naturel ou -1 - Le nombre de tentatives autorisees par etudiants pour ce scenario (-1 -> nombre de tentatives infinies)
            _delay : Entier naturel - Le delai minimum entre deux tentative de test de ce scenario pour un etudiant
            _visible : bool - Indique si le scénario est visible ou non par l'étudiant
            _mark : Entier naturel - Le nombre total de points a evaluer sur ce scenario
    '''

    @argumentType("_run", types.FunctionType)
    @argumentType("_nb_attempts", int)
    @argumentType("_delay", int)
    @argumentType("_visible", bool)
    @argumentType("_mark", int)
    def __init__(self, _run, _nb_attempts=INFINITE_ATTEMPTS, _delay=DELAY, _visible=True, _mark=0):

        self.run = _run 
        self.nb_attempts = _nb_attempts
        self.delay = _delay
        self.visible = _visible
        self.mark = _mark

    def getName(self):
        return self.run.__name__