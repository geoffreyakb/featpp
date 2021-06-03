# Modules Python
import datetime
import sqlite3
import sys
import re
from jinja2 import Template
import functools

# Modules featpp
from Scenario import Scenario, INFINITE_ATTEMPTS
from ToolResult import ToolResult
from Text import Text
from Penalty import Penalty
from typeAnnotations import *
from Result import Result


# Fichier stockant les paths utiles
from variables import *


class CompromisedFileException(Exception):
    
    '''
        Exception créée pour gérer le fichier modalité compromis d'un étudiant.
    '''
    
    pass


@argumentType("scenarios", {list: Scenario})
@argumentType("student_name", str, True)
@argumentType("database_address", str)
@returnType(str)
def modalities_text(scenarios, database_address, student_name=None):
    
    '''
        Cette fonction génère le fichier de modalités à l'initialisation lorsque
        student_name est None et pour un étudiant lorsque student_name est un string

        Paramètres de la fonction :
            scenarios : Scenario[] - Liste totale des scénarios demandés par l'enseignant dans 
                                     le fichier de configuration.
            database_address : String - Chemin vers la base de données
            student_name : String - Identifiant de l'étudiant dans la bdd, par défaut a None.    
        
    '''
    # Lecture du template des modalités
    txt = os.path.join(featpp_path, "main", "resource", "modalites.txt")
    with open(txt, "r") as txt:
       template = Template(txt.read())

    if(student_name == None):

        # Création des valeurs par défaut
        sc_data = [
            ( s.getName(), s.visible, "non", s.nb_attempts, 
            datetime.datetime.today(), datetime.datetime.today(), 0) for s in scenarios
        ]
        # Création du rendu
        return template.render(
            choice_all = "non",
            choice_all_not_limited = "non",
            scenario_data = sc_data
        )

    else:

        sc_data = []

        # Récupération des informations en bdd
        con = sqlite3.connect(database_address)
        cur = con.cursor()

        for s in scenarios:
            cur.execute("SELECT Attempts, Date, Attempts_Done FROM " + s.getName() + " WHERE Students='%s'" % student_name)
            result = cur.fetchone()
            date = datetime.datetime.strptime(result[1], "%Y-%m-%d %H:%M:%S.%f")
            nextdate = str(date + datetime.timedelta(seconds = s.delay))
            attempts = int(result[0])
            attempts_done = int(result[2])
            sc_data += [( s.getName(), s.visible, "non", attempts, date, nextdate, attempts_done)]
            
        # Création du rendu
        return template.render(
            choice_all = "non",
            choice_all_not_limited = "non",
            scenario_data = sc_data
        )
    

@argumentType("scenarios", {list: Scenario})
@argumentType("modalities_address", str)
@returnType({dict : (str, str)})
def parse_modalities(modalities_address, scenarios):
    
    """
        /!\ /!\ TODO - A COMPLETER /!\ /!\

        Paramètres de la fonction :
            modalities_address : String - Chemin vers le fichier de modalités
            scenarios : Scenario[] - A COMPLETER
    """

    # Ouverture du template
    txt = os.path.join(featpp_path, "main", "resource", "modalites.txt")
    with open(txt, "r") as txt:
       template = Template(txt.read())

    # Développement du template
    subtemplate = template.render(
        choice_all = "{{choice_all}}",
        choice_all_not_limited = "{{choice_all_not_limited}}",
        scenario_data = [ (s.getName(), s.visible, "{{" + s.getName() + "}}", 0, "", "", 0) for s in scenarios]
    ).split("\n")

    # Conversion des données du fichier élève
    answers = {}
    with open(modalities_address, "r") as mod_file:
        studenttxt = mod_file.readlines()

    for i in range(len(subtemplate)):
        r = re.search("(.*)\{\{([a-zA-Z_0-9]+)\}\}", subtemplate[i])
        if(r != None):
            if(len(studenttxt) <= i):
                raise CompromisedFileException
            if(r.group(1) != studenttxt[i][:len(r.group(1))]):
                raise CompromisedFileException
            studenttxt[i] = studenttxt[i][len(r.group(1)):]
                
            r2 = re.search("(oui|non)", studenttxt[i], flags=re.IGNORECASE)
            if(r2 == None):
                raise CompromisedFileException
            answers[r.group(2)] = r2.group(1)
                
    return answers


@argumentType("modalities_address", str)
@argumentType("scenarios", {list: Scenario})
@returnType({list: Scenario})
def get_scenarios(modalities_address, scenarios):
    
    """
        Cette fonction permet de récuperer les scénarios qui doivent être joués
        à partir d'un fichier modalités d'un élève, en le comparant au template 
        de modalités. Si jamais l'étudiant a fait des modifications qui perturbent 
        la détection, une exception est levée.

        Paramètres de la fonction :
            modalities_address : String - Chemin vers le fichier modalités de l'étudiant
            scenarios : Scenario[] - Liste de scénarios disponibles
    """
    
    new_scenarios = []
    answers = parse_modalities(modalities_address, scenarios)

    # Création de l'association nom - scenario
    scs = {}
    for s in scenarios:
        scs[s.getName()] = s

    # Cas ou l'étudiant souhaite tous les resultats
    if(answers["choice_all"] == "oui"):
        for s in scenarios:
            if(s.visible):
                new_scenarios += [s]
        return new_scenarios

    # Autres cas
    if(answers["choice_all_not_limited"] == "oui"):
        for s in scenarios:
            if(s.visible and s.nb_attempts == INFINITE_ATTEMPTS):
                new_scenarios += [s]
    
    for elt, ans in answers.items():
        if(elt in scs.keys() and elt not in new_scenarios):
            if(ans == "oui"):
                new_scenarios += [scs[elt]]

    return new_scenarios


@argumentType("scenarios", {list: Scenario})
@argumentType("student_name", str)
@argumentType("database_address", str)
@argumentType("modalities_address", str)
@argumentType("SCENARIOS", {list: Scenario})
@returnType({list: {list: Result}})         
def run_scenarios(scenarios, database_address, modalities_address, student_name, project_env, SCENARIOS) :
    
    """
        Cette fonction a pour but principal d'exécuter tous les scénarios donnés.
        Elle va de plus mettre à jour la base de données au niveau des dates et
        du nombre de tentative. Enfin, elle met à jour le fichier modalites.txt des 
        étudiants.

        Paramètres de la fonction :
            scenarios : Scenario[] - La liste des scénarios à jouer
            database_address : String - Chemin vers la base de données
            modalities_address : String - Chemin vers le fichier de modalités
            student_name : String - L'identifiant de l'étudiant dans la bdd
            project_env : ProjectEnv - Environnement du projet
            SCENARIOS : Scenario[] - La liste de tous les scénarios fournie par le fichier de configuration
    """

    results = []
    # Ouverture de la bdd
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    for scenario in scenarios :
        # Exécution d'un scénario
        results.append(scenario.run(project_env))
        # Récupération du nombre de tentatives et éventuelle modification s'il n'est pas infini
        cur.execute("SELECT Attempts FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
        attempts = int(cur.fetchone()[0])
        if (attempts != -1):
            attempts += -1
            # Mise à jour du nombre de tentatives si nécessaire
            cur.execute("UPDATE " + scenario.getName() + " SET Attempts = '" + str(attempts) + "' WHERE Students = '%s'" % student_name)
        # Mise à jour de la dernière date d'utilisation du scénario dans la bdd
        cur.execute("UPDATE " + scenario.getName() + " SET Date = '" + str(datetime.datetime.today()) + "' WHERE Students = '%s'" % student_name)
        # Mise à jour du nombre de tentatives effectués pour ce test
        cur.execute("SELECT Attempts_Done FROM " + scenario.getName() + " WHERE Students = '%s'" % student_name)
        attempts_done = int(cur.fetchone()[0])
        cur.execute("UPDATE " + scenario.getName() + " SET Attempts_Done = '" + str(attempts_done + 1) + "' WHERE Students = '%s'" % student_name)
    # Mise à jour et fermeture de la bdd
    con.commit()
    con.close()
    # Ecriture du fichier modalites.txt avec les nouvelles valeurs de la bdd
    with open(modalities_address, "w") as writer:
        writer.write(modalities_text(SCENARIOS, database_address, student_name))
    return results

@argumentType("scenarios", {list: Scenario})
@argumentType("results", {list: {list: Result}})
@argumentType("student_name", str)
@argumentType("database_address", str)
@returnType({list: Result})   
def report(scenarios, results, database_address, student_name):
    
    """
        Cette fonction a pour but de créer une liste de Result qui devra être ajoutée à
        la liste de liste de Result obtenue par run_scenarios. Cette nouvelle liste
        permet l'affichage d'un compte-rendu des scores obtenus sur les scénarios joués.

        Paramètres de la fonction :
            scenarios : Scenario[] - La liste des scénarios à jouer
            results : Result[][] - La liste des résultats obtenus par run_scenarios
            database_address : String - Chemin vers la base de données
            student_name : String - L'identifiant de l'étudiant dans la bdd
    """
    
    # Ouverture de la base de données
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    
    # Initialisation du rapport contenant les scores obtenus pour chaque scénario joué
    score_report = [Text("Compte-rendu concernant les scenarios joues", 6)]
    
    # Compteur de pénalités pour tous les scénarios joués
    penalties_sum = 0
    
    # Score obtenu pour tous les scénarios joués
    score_sum = 0
    
    # Pour chaque scénario joué
    for i in range(len(scenarios)):
        s = scenarios[i]
        # Compteur de pénalité pour un scénario
        penalty = 0
        score_sum += s.mark
        # Pour chaque résultat obtenu pour ce scénario
        for r in results[i]:
            # Si on trouve une pénalité, on incrémente les compteurs de pénalités
            if isinstance(r, Penalty):
                penalty += r.penalty
                penalties_sum += r.penalty
                
        # Comparaison du score obtenu pour ce cycle avec celui que l'étudiant avait obtenu au cycle précédent
        cur.execute("SELECT Mark FROM " + s.getName() + " WHERE Students = '%s'" % student_name)
        last_mark = int(cur.fetchone()[0])
        current_mark = s.mark - penalty
        
        # Ecriture du message pour indiquer la progression de l'étudiant
        message = s.getName() + " - Vous avez obtenu " + str(current_mark) + "/" + str(s.mark)
        if last_mark < current_mark:
            message += ". C'est mieux que la derniere fois ! (" + str(last_mark) + "/" + str(s.mark) + ")"
        elif last_mark == current_mark:
            message += " comme la derniere fois."
        else:
            message += ". C'est moins bien que la derniere fois. (" + str(last_mark) + "/" + str(s.mark) + ")"
        score_report.append(Text(message))
        
        # Mise à jour de la base de données
        cur.execute("UPDATE " + s.getName() + " SET Mark ='" + str(current_mark) + "' WHERE Students = '%s'" % student_name)
        cur.execute("UPDATE " + s.getName() + " SET Penalty ='" + str(penalty) + "' WHERE Students = '%s'" % student_name)
    
    # Calcul et ajout du score global obtenu pour les scénarios joués
    score_report.append(Text("Score pour les scenarios joues : " + str(score_sum - penalties_sum) + "/" + str(score_sum) + ".\n"))
    
    # Mise à jour effective et fermeture de la base de donnée
    con.commit()
    con.close()
    return score_report


@argumentType("results", {list:{list: Result}})
@argumentType("dest_file", str)
@argumentType("mode", int)
def print_results(results, dest_file, mode) :
    
    """
        Cette fonction a pour but principal d'appeler les print_result des
        classes d'affichage pour créer les fichiers de rendus détaillés ou synthétiques.

        Paramètres de la fonction :
            results : Result[][] - Liste contenant des listes de Result pour générer l'affichage
            dest_file : String - La localisation du fichier dans lequel écrire les résultats
            mode : Int - Le mode d'écriture (détaillé, synthétique, ...) 
    """
    
     # Réinitialisation du fichier de destination
    with open(dest_file , "w") as writer:
        writer.write("")
    
    # Pour chaque test effectué, écriture dans le fichier de destination
    for list_result in results :
        for result in list_result :
            result.print_result(dest_file, mode)


@argumentType("database_address", str)
@argumentType("students_list", {list: str})
@argumentType("scenarios_list", {list: Scenario})
@returnType(str)        
def print_overall_progress(database_address, students_list, scenarios_list):
    
    """
        Cette fonction a pour but principal de rédiger le contenu du fichier avancee_globale.txt
        qui sera fourni à l'enseignant lorsqu'il en fera la demande. Cette fonction utilise le template 
        fourni dans le dossier resource : avancee_globale.txt et créera le texte d'un fichier qui sera présent
        dans le dossier du projet de l'enseignant au même niveau que config.py et la base de données.

        Paramètres de la fonction :
            database_address : String - Chemin vers la base de données
            students_list : str[] - La liste des scénarios à jouer
            scenarios_list : Scenario[] - La liste des scénarios du projet
    """
    # Cas illégaux
    if students_list == []:
        return "La liste des etudiants est vide."
    if scenarios_list == []:
        return "La liste des scenarios est vide."
    
    # Ouverture de la base de données
    con = sqlite3.connect(database_address)
    cur = con.cursor()
    
    # Lecture du template de l'avancée globale
    text = os.path.join(featpp_path, "main", "resource", "avancee_globale.txt")
    with open(text, "r") as text:
        template = Template(text.read())
    
    # Création des data
    stud_data = {}
    scores = []
    max_score = 0
    
    # Score maximum que peut avoir un étudiant pour ces scénarios
    for s in scenarios_list:
        max_score += s.mark
        
    # Pour chaque élève, on crée un dictionnaire {nom_du_scenario:score_obtenu} de la forme score/note_du_scenario (pourcentage_équivalent%} nb_tentatives tentative(s)
    for student in students_list:
        data = {}
        score = 0
        for scenario in scenarios_list:
            # Récupération de la note de l'élève sur un scénario donné
            cur.execute("SELECT Mark, Attempts_Done FROM " + scenario.getName() + " WHERE Students = '" + student + "';")
            result = cur.fetchone()
            mark = result[0]
            attempts_done = result[1]
            if attempts_done == '0' or attempts_done == '1':
                attempts_msg = ' tentative'
            else:
                attempts_msg = ' tentatives'
            score += int(mark)
            if scenario.mark != 0:
                percentage = (int(mark)/scenario.mark)*100
            else:
                percentage = 100.0
            data[scenario.getName()] = mark + ' / ' + str(scenario.mark) + ' (' + str(percentage) + '%) ' + attempts_done + attempts_msg 
        # Une fois le dictionnaire d'un élève rempli, on l'ajoute à un dictionnaire {nom_eleve:dictionnaire_eleve}
        stud_data[student] = data
        
        # En même temps, on calcule le score global obtenu pour chaque élève et on stocke cette information dans scores
        if max_score != 0:
            total_percentage = (score/max_score)*100
        else:
            total_percentage = 100.0
        scores.append((student, str(score) + ' / ' + str(max_score) + ' (' + str(total_percentage) + '%)'))
    # On trie la liste en fonction des notes croissantes pour repérer les élèves en difficultés en premier.
    scores.sort(key=lambda x: int(x[1].split()[0]), reverse=False)
    
    
    # Fermeture de la base de données
    con.close()
    
    # Création du rendu
    return template.render(
        date = datetime.datetime.today().strftime("%Y-%m-%d_%Hh%Mm%Ss"),
        scores_data = scores,
        students_data = stud_data,
        scenarios_data = [s.getName() for s in scenarios_list] 
    )