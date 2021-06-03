# Manuel utilisateur FEAT++ - Professeurs

Ce manuel est destiné à être utilisé par les professeurs qui souhaiteraient utiliser le framework FEAT++. Il explique comment installer le framework sur une machine, comment utiliser les différentes commandes que FEAT++ propose et comment configurer les fichiers nécessaires au bon fonctionnement du framework.

#### Table des matières

I. [Installation du framework](#installation)
II. [Commandes](#commandes)
	A. [Créer un nouveau projet vierge](#startup)
	B. [Configurer un projet](#setup)
	C. [Vérifier ses propres scripts de tests](#runtests)
	D. [Récupérer le travail sur demande d'un élève](#mill)
	E. [Lancer un cycle de tests](#cycle_teacher)
	F. [Obtenir un aperçu de l'avancée globale des étudiants](#progress)
III. [Documents utiles](#documents)
	A. [Fichier de configuration : config.py](#config)
	B. [Fichiers relatifs aux scripts de tests](#script)
	C. [Fichier de modalités : modalites.txt](#modalites)
    D. [Fichier d'avancée globale : avancee_globale_[DATE].txt](#avancee)
	E. [Fichiers de retour : synthese.txt et details.txt](#retour)


## I. Installation du framework  <a id='installation'></a>

### Prérequis 
Avant d'installer ce programme, il est nécessaire :
- D'être sur une distribution Debian de linux.
- D'avoir installé `python3` et un compilateur C (par exemple `gcc`)

### Comment installer  FEAT++ ?
* Si aucune modification n'a été apportée au code du projet, il suffit de se placer à la racine du projet et d'exécuter la commande : 

  ```bash
  sudo dpkg -i install/featpp.deb
  ```

* Si jamais le code du dépôt a été modifié, il faut se placer à la racine du projet et exécuter la commande 

  ```bash
  sh install.sh
  ```

  Ce script recrée le package `.deb` avant de l'installer.

## II. Commandes  <a id='commandes'></a>

#### A. Créer un nouveau projet vierge  <a id='startup'></a>

Afin de créer un nouveau projet, l'enseignant peut utiliser la commande suivante :

```bash
featpp startup <dossier_projet>
```

Argument :

* dossier_projet : Il s'agit du dossier qui sera créé et qui contiendra l'arborescence par défaut d'un nouveau projet sous FEAT++.

Cette commande va générer une arborescence par défaut d'un projet sous FEAT++ :

```txt
Projet
├── config.py
├── public
│   ├── retours
│   └── sources
│       └── HelloWorld.java
├── scriptsTests
└── testsProject
```

Cette arborescence contient les éléments suivants :

* __config.py__ est le fichier de configuration du projet. C'est dans ce dernier qu'il est possible de définir des scénarios de tests qui pourront être joués sur le code d'un étudiant. Ces scénarios sont écrits en langage python et des informations plus détaillées sur la configuration de ce fichier peuvent être trouvés en section [Documents utiles](#config).
* __public__ est un dossier contenant tous les fichiers que l'élève devrait pouvoir récupérer sur son dépôt. Il contient :
  * __sources__ qui est un dossier qui devrait contenir les sources fournies par l'enseignant pour le projet. 
  * __retours__ qui est un dossier qui contiendra les retours fournis par le framework sur le code de l'élève vis-à-vis du fichier de configuration.
* __scriptsTests__ est un dossier contenant des fichiers rédigés par l'enseignant qui serviront d'entrée pour les outils de tests (Ex : classes de tests JUnit, paramètres checkstyle, ...)
* __testsProject__ est un dossier qui contiendra des tests que l'enseignant pourra réaliser sur le code qu'il fournit pour faire des vérifications. Vous trouverez plus d'informations sur ce point dans la section [Vérifier ses propres scripts de tests](#runtests).

### B. Configurer un projet  <a id='setup'></a>

Pour configurer un projet, il faut modifier le fichier `config.py`, éventuellement fournir des fichiers utiles pour les tests, éventuellement fournir des fichiers pour tester les sources qu'il fournit. Vous trouverez plus d'informations sur la manière de configurer tous ces documents dans la section [Documents utiles](#documents). Une fois que la configuration a été effectuée, il est possible de la mettre en pratique en utilisant la commande suivante :

```bash
featpp setup <dossier_projet> <liste_etudiant>
```

Arguments :

* dossier_projet : Il s'agit du dossier dans lequel se trouvent le fichier de configuration `config.py` et la base de donnée `database_test.db` relatifs au projet pour lequel le professeur souhaite obtenir l'avancée globale des étudiants. 

* liste_eleve : Il s'agit d'un fichier au format `.csv` qui contient la liste des élèves dont on souhaite connaître la progression. Cette liste doit être rédigée sous le format suivant :

```txt
Students
student1
student2
student3
```

Cette commande va générer deux nouveaux fichiers :

* __modalites.txt__ : Il s'agit du fichier qui va permettre à l'étudiant de définir les scénarios de tests qu'il veut jouer. Plus d'informations disponibles [ici](#modalites). Ce fichier est généré dans le dossier __public__.
* __database_test.db__ : Il s'agit de la base de données propre au projet et au fichier de configuration fourni. C'est une base créée avec `sqlite3` qui contient une table par scénario de tests et des informations importantes comme le nombre de tentatives effectuées, le nombre de tentatives restantes, la dernière date d'exécution du scénario, le score et les pénalités obtenus pour un étudiant.

### C. Vérifier ses propres scripts de tests  <a id='runtests'></a>

Pour configurer les tests d'un projet, il faut modifier le fichier `testsProject/tests_runner.py`, et optionnellement ajouter des scénarios de test dans le fichier `config.py`. Vous trouverez plus d'informations sur la manière de configurer tous ces documents dans la section [Documents utiles](#documents). Une fois que la configuration a été effectuée, il est possible de la mettre en pratique en utilisant la commande suivante :

```bash
featpp runtests <dossier_projet>
```

Argument :

* dossier_projet : Il s'agit du dossier dans lequel se trouve le fichier de configuration `config.py` relatif au projet pour lequel le professeur souhaite exercer ses tests. 


### D. Récupérer le travail sur demande d'un élève  <a id='mill'></a>

Une fois que tout a été configuré, l'utilisateur n'a plus qu'à lancer la commande suivante pour activer la détection automatique des demandes d'évaluation :

```bash
featpp mill <racine_depot> <dossier_projets>
```

Arguments :

* racine_depot : Le chemin vers le dossier contenant les dépôts Subversion de tout les élèves. 
* dossiers_projets : Le chemin vers le racine contenant tout les TPs et projets créés par l'enseignant.

Dans les faits, cette commande va régulièrement effectuer les commandes **svn update** et **svn info** afin de mettre à jour les dépôts, puis de vérifier si le fichier de modalités a été modifié depuis le dernier cycle de tests, auquel cas un cycle de tests est lancé. Le délai d'attente entre deux vérifications des sources des élèves est de 5 secondes par défaut. Celui-ci peut être changé depuis la variable **WAIT_TIME** dans le fichier `main_mill.py`.

En théorie, mill n'a pas besoin d'être relancé après la création de chaque nouveau TP ou projet car il effectue une vérification à partir des dossiers présents dans le dépôt de chaque élève. Toutefois, cette fonctionnalité n'a pas été complètement testée et il est recommandé à l'utilisateur de stopper puis relancer le mill quand un nouveau travail est ajouté.   

### E. Lancer un cycle de tests  <a id='cycle_teacher'></a>

Il est possible pour le professeur de lancer un cycle de test pour un élève sans tenir compte de ses contraintes afin de vérifier ce que l'élève a produit à la main. Pour cela il faut utiliser la commande suivante :

```bash
featpp cycle_teacher <dossier_projet> <dossier_projet_etudiant> <scenario1> <scenario2> ...
```

Arguments :

* dossier_projet : Il s'agit du dossier dans lequel se trouve le fichier de configuration `config.py` concernant le projet que le professeur souhaite tester chez l'élève.

* dossier_projet_etudiant : Il s'agit du dossier du projet en question mais dans le dossier de l'élève concerné.

* une liste de noms de scenario que le professeur souhaite voir testé chez l'élève.

### F. Obtenir un aperçu de l'avancée globale des étudiants  <a id='progress'></a>

Plutôt que d'observer un à un chaque dossier d'un élève pour voir où ils en sont, il est possible de générer un fichier texte contenant une synthèse de la progression des élèves en utilisant la commande suivante :

```bash
featpp progress <dossier_projet> <liste_eleves>
```

Arguments :

* dossier_projet : Il s'agit du dossier dans lequel se trouvent le fichier de configuration `config.py` et la base de donnée `database_test.db` relatifs au projet pour lequel le professeur souhaite obtenir l'avancée globale des étudiants. 
* liste_eleve : Il s'agit d'un fichier au format `.csv` qui contient la liste des élèves dont on souhaite connaître la progression. Cette liste doit être rédigée sous le format suivant :
  

```txt
Students
student1
student2
student3
```

Un fichier nommé `avancee_globale_[DATE].txt` est alors généré dans le dossier du projet avec __[DATE]__ écrit au format `%Y-%m-%d_%Hh%Mm%Ss`. Pour avoir un aperçu de ce fichier, vous pouvez vous rendre [ici](#avancee).

## III. Documents utiles <a id='documents'></a>

### A. Fichier de configuration : config.py  <a id='config'></a>

Le fichier de configuration d'un projet est la principale interface entre FEAT++ et le professeur. Il s'agit d'un fichier python config.py dont un exemple est donné lors de l'initialisation du projet. Il commence par les importations nécessaires à son bon fonctionnement. A noter que _from tools import *_ permet d'importer tous les outils disponibles grâce à FEAT++.

```
from Scenario import Scenario
from tools import *
from Text import Text
```

Puis il faut instancier les outils qui vont servir pour le projet, par exemple :

```
javaCompiler = JavaCompiler() 
blackBox = Blackbox()
```

Puis le professeur doit définir des scénarios de test. Pour cela il doit créer une fonction python par scénario. Cette fonction permet de définir concrètement quel test exécute le scénario et dans quel ordre. 

Le professeur est libre d'utiliser la syntaxe python pour y mettre des conditionnels par exemple.

En voici un exemple :

```
def scenario_example(project_env):
    results = [
    run = javaCompiler.run(project_env, ["HelloWorld.java"])
    if run.result == "ERROR" :
        result.append(Penalty("Pénalité : 1 point perdu", 1))
    else 
        results.append(blackBox.run(project_env, "helloWorld"))
    
    return results
```
Le professeur peut ajouter des pénalités selon les résultats des différents tests comme on peut le voir dans l'exemple précédent. Afin d'être le plus flexible possible, le professeur peut se renseigner sur les différents attributs des différents objets dans le `README_DEV.md`



Après avoir défini l'ensemble de ces fonctions, le professeur doit créer les scénarios à proprement parler et les ajouter dans une liste à la fin du fichier de configuration. 

Pour créer un scénario, il y a plusieurs paramètres :

* **_run**, une fonction (celle définie préalablement) qui correspond à ce que fait concrètement le scénario.

* **_nb_attempts**, un entier correspondant au nombre de fois maximum qu'un élève peut demander à exécuter ce scénario. Par défaut fixé à l'infini.

* **_delay**, un entier correspondant au nombre de secondes définissant la limite de fréquence de demande d'exécution de ce scénario. Par défaut fixé à une variable globale DELAY = 5.

* **_visible**, un booléen indiquant si le scénario sera ou non visible pour l'étudiant. Cela peut être utile pour des tests particuliers, d'évaluation par exemple. Par défaut fixé à vrai. 

* **_mark**, un entier indiquant combien de points au total représente le scénario, utile si le professeur décide d'utiliser des pénalités. Par défaut fixé à 0.

Ainsi, à la fin du fichier de configuration, on trouve deux listes : 

La première correspond aux scenarios qui vont réellement faire partie du projet : 
```
SCENARIOS = [
    Scenario(scenario1),
    Scenario(scenario2),
    Scenario(scenario_example, _visible = false, _mark = 5)
]
```

La seconde correspond aux scenarios utilisés par le professeur pour tester ses propres fichiers en interne avec la commande **runtests** : 

```
SCENARIOS_TESTS = SCENARIOS + [
    Scenario(scenario_test),
    Scenario(bad_scenario_test),
]
```

#### Note concernant la sécurité de la machine lors de l'exécution du code d'un étudiant

Cette section n'a d'intérêt que lorsque le besoin de redéfinir ponctuellement la fonction `run()` d'un outil se présente (ce qui devrait ne se produire que peu). Hors de ce cas de figure, cette section peut être ignorée. Cette section relève plus du développement que de l'utilisation, mais présente des problèmes pouvant être rencontrés par les enseignants.

Afin d'assurer la sécurité des machines des enseignants, tout code auquel on ne peut pas faire confiance (notamment celui des étudiants) doit être exécuté dans un environnement isolé.
Ainsi, si la fonction `run()` d'un outil exécutant un code auquel on ne fait pas confiance est redéfinie, les appels d'exécution de ce code doivent se faire avec la fonction `isolate_run(id, options, prog)` définie dans le fichier `isolate.py`, `id` étant accessible depuis l'attribut `ProjectEnv.isolate_id`, `options` permettant de contrôler les restrictions appliquées sur le code exécuté (cf. http://www.ucw.cz/moe/isolate.1.html), et `prog` contenant un appel en ligne de commande de syntaxe similaire à celui de `SubProcess.run()`.
À noter cependant que toutes les sources et les fichiers avec lesquels le code doit interagir au cours de son exécution doivent avoir été déplacés dans le dossier correspondant à l'environnement isolé avant l'exécution. L'intégralité du dossier source de l'étudiant est déplacée au début du cycle de tests, cependant tout fichier nécessaire et extérieur au dossier source de l'étudiant doit être déplacé à l'aide de la fonction `isolate_mv(isolated_dir, files)`, `isolated_dir` étant accessible depuis l'attribut `ProjectEnv.path_to_isolate_env`, et `files` étant une liste de chemins (absolus ou relatifs à l'environnement d'exécution de FEAT++) vers les fichiers/dossiers à déplacer.
À noter également que les appels de commandes externes à l'environnement isolé (par exemple `sh` ou `java`) par la fonction `isolate_run(id, options, prog)` doivent être fait avec le chemin absolu de l'exécutable (par exemple : `/usr/bin/sh` ou `/usr/bin/java`), et que les chemins vers des fichiers dans l'environnement isolé dans la commande passée dans le paramètre `prog` doivent être relatifs à la racine de l'environnement isolé (par exemple : "src/TP_java/HelloWorld.java").
Un problème peut survenir dans le cas où le chemin absolu donné pour un exécutable est en réalité un lien symbolique. Le problème peut être contourné en utilisant la commande `realpath` ou `readlink` (par exemple : `$(/usr/bin/realpath /usr/bin/java)`), ou en remplaçant le chemin par le contenu d'une variable d'environnement dans laquelle le chemin réel a été enregistré au préalable (par exemple : `PATHTOJAVA=$(realpath $(which java))`).

### B. Fichiers relatifs aux scripts de tests  <a id='script'></a>

#### B.1 Les fichiers du dossier ScriptsTests  <a id='ScriptsTests'></a>

Ce dossier contient tous les fichiers qui vont devoir être appelé par les outils et qui ne seront pas chez l'étudiant. Par exemple pour les tests en boîte noire, on trouvera ici les fichiers qui permettront de comparer le résultat et qui doivent se terminer par `.expected` et les fichiers qui permettent de décrire ce que doit executer le test en boite noire, ceux-ci doivent se terminer par `.run`. En voici deux exemples :

__exempleConfiantTricheurSujet.run__

```bash
#!/bin/bash
/usr/lib/jvm/java-11-openjdk-amd64/bin/java allumettes.Partie -confiant Ordinateur@rapide Tricheur@tricheur << EOF
EOF
```

Pour l'instant, il faut mettre le chemin complet pour appeler des logiciels.

__exempleConfiantTricheurSujet.expected__

```
Nombre d'allumettes restantes : 13
Au tour de Ordinateur.
Ordinateur prend 3 allumettes.

Nombre d'allumettes restantes : 10
Au tour de Tricheur.
Tricheur prend 1 allumette.

Nombre d'allumettes restantes : 1
Au tour de Ordinateur.
Ordinateur prend 1 allumette.
Ordinateur a perdu !
Tricheur a gagné !
```

#### B.2 Les fichiers du dossier TestsProject  <a id='TestsProject'></a>

Le but de ce dossier est de permettre l'utilisation de la commande **runtests**. Le fichier le plus important de ce dossier est  `tests_runner.py`. Celui-ci contient un dictionnaire python qui permet de préciser quel scenario de quel dossier doit bien s'exécuter ou doit mal s'exécuter. En effet, pour vérifier le bon fonctionnement de son projet, le professeur peut simuler le code des élèves de telle sorte que les résultats des scénarios de tests doivent être positifs ou négatifs. 

Ce fichier est en directe corrélation avec la liste __SCENARIOS_TESTS__ définie dans le fichier config.py. Le professeur a connaissance des scénarios qu'il a placés dans cette liste pour ses tests personnels.

Ce dictionnaire est écrit comme suit :

```
TESTS = {
    "ExampleTestOK" : True,
    "ExampleTestKO" : {
        "scenario2" : True,
        "scenario_test" : False,
        "bad_scenario_test" : False
    },
}
```

__ExampleTestOk__ est un dossier qui contient une simulation de fichier source d'un élève tel que tous les tests de __SCENARIOS_TESTS__ doivent bien s'exécuter.

__ExampleTestKO__ est un dossier qui contient une simulation de fichier source d'un élève tel que le scenario2 doit bien s'exécuter tandis qu'il doit y avoir au moins une erreur en exécutant les deux autres.




### C. Fichier de modalités : modalites.txt <a id='modalites'></a>

Le fichier `modalites.txt` est généré lors de la [configuration d'un projet](#config). Le fichier de modalités est le support que les étudiants utilisent pour demander une évaluation de leur code. Ce fichier contient plusieurs blocs de textes, chacun relatif à un scénario de tests écrit par un professeur. Chaque bloc de texte contient le nom du scénario, la dernière date d'utilisation de ce scénario, la prochaine date à laquelle il pourra être relancé et enfin le nombre de tentatives restantes et déjà effectuées. Pour identifier les scénarios qu'un étudiant veut jouer, il suffit que ce dernier remplace le terme "non" écrit à côté du nom du scénario par "oui". Il est aussi possible de jouer tous les scénarios en remplaçant "non" par "oui" sur la première ligne du fichier de modalités, ainsi que de ne jouer que les scénario sans restriction du nombre de tentatives en remplaçant "non" par "oui" sur la deuxième ligne du fichier. Voici un exemple de fichier de modalités :

```txt
Voulez-vous jouer tous les tests ? non
Voulez-vous jouer tous les tests qui n'ont pas de restriction de tentatives (infini) ? non

scenario1 : non
    nombre de tentatives infini, vous avez joue ce test 3 fois
    derniere tentative = 2021-03-03 15:52:16.828228
    prochaine tentative possible = 2021-03-03 15:52:21.828228

scenario2 : non
    nombre de tentatives restantes = 10
    derniere tentative = 2021-03-03 15:52:16.828228
    prochaine tentative possible = 2021-03-03 15:52:21.828228
```

Si jamais un étudiant modifie et compromet ce fichier en supprimant ou ajoutant une ligne ou s'il écrit autre chose que "oui" ou "non", alors ce dernier est prévenu de la compromission, aucun scénario n'est joué et le fichier de modalité est réinitialisé. 

### D. Fichier d'avancée globale : avancee_globale_[DATE].txt <a id='avancee'></a>

Pour générer un fichier `avancee_globale_[DATE].txt`, référez-vous à [cette partie](#progress). Un fichier d'avancée globale contient la progression des étudiants vis-à-vis du score obtenu par scénario. Cette progression est exprimée scénario par scénario et enfin pour la totalité des scénarios. De plus, il est possible d'observer le nombre de tentatives effectuées pour chaque scénario pour chaque élève. Voici un exemple de fichier d'avancée globale :

```txt
Date d'execution : 2021-03-03_15h52m25s

scenario1
-------------------------------------------
Eleve1 : 2/5 (40.0%) 3 tentatives
-------------------------------------------
Eleve2 : 3/5 (60.0%) 5 tentatives
-------------------------------------------
Eleve3 : 5/5 (100.0%) 2 tentatives
-------------------------------------------

scenario2
-------------------------------------------
Eleve1 : 3/5 (60.0%) 3 tentatives
-------------------------------------------
Eleve2 : 0/5 (0.0%) 0 tentative
-------------------------------------------
Eleve3 : 4/5 (80.0%) 1 tentative
-------------------------------------------

Score total obtenu par les etudiants :
-------------------------------------------
Eleve1 : 5/10 (50.0%)
-------------------------------------------
Eleve2 : 3/10 (30.0%)
-------------------------------------------
Eleve3 : 9/10 (90.0%)
-------------------------------------------
```

### E. Fichiers de retour : synthese.txt et details.txt <a id='retour'></a>