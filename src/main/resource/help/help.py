class HelpDefinition():


    def __init__(self, _title, _description):
        self.title = _title
        self.description = _description
        self.args = []
    
    def add_arg(self, _arg, _description):
        self.args.append(_description)

    def __str__(self):
        txt = "| " + self.title + " : " + self.description + "\n"
        for i in range(len(self.args)):
            desc = self.args[i]
            txt += "├── arg" + str(i) + " : " + desc + "\n"
        txt += "\n\n"
        return txt

Help_setup = HelpDefinition("setup", "Met en place votre environnement en créant les dossiers avec les paths rentrés dans le fichier .json si ce n'est pas déjà fait")
Help_setup.add_arg("Le path du fichier .json")

Help_start = HelpDefinition("start", "Débute la création d'un nouveau projet")
Help_start.add_arg("Le nom de ce nouveau projet")

Help_runtests = HelpDefinition("runtests", "Permet d'effectuer des tests sur un projet déjà configurer avant de l'envoyer à vos élèves")
Help_runtests.add_arg("Le nom du projet à tester")

Help_send = HelpDefinition("send", "à utiliser après avoir configurer et tester votre projet : la commande envoie le projet sur le svn de vos étudiants")
Help_send.add_arg("Le nom du projet à déployer")
Help_send.add_arg("Les noms des promos auxquelles envoyer le projet (all pour toutes)")

Help_evaluate= HelpDefinition("evaluate", "Lance des batteries de tests sur un étudiant et un TP en particulier")
Help_evaluate.add_arg("La promo de l'étudiant")
Help_evaluate.add_arg("Le login de l'étudiant (ou le nom de son dépôt svn)")
Help_evaluate.add_arg("Le nom du projet")

Help_progress= HelpDefinition("progress", "Permet à l'enseignant de récupérer des informations sur l'avancée des étudiants dans un fichier avancee_globale.txt")
Help_progress.add_arg("Le nom du projet")
Help_progress.add_arg("Les noms des promos pour lesquelles on veut savoir l'avancée (all pour toutes)")

Help_shut = HelpDefinition("shut", "Permet de finir un projet pour une promo donnée, et ainsi l'enseignant ne recevra plus les avancées et demandes de tests des étudiants")
Help_shut.add_arg("Le nom du projet à finir")
Help_shut.add_arg("Les noms des promos pour lesquelles le projet est terminé (all pour toutes)")

HelpS = {
    "setup" : Help_setup,
    "start" : Help_start,
    "runtests" : Help_runtests,
    "send" : Help_send,
    "evaluate" : Help_evaluate,
    "progress" : Help_progress,
    "shut" : Help_shut
}