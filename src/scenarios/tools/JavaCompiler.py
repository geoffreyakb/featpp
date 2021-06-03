from Tool import Tool, select_arg
from JavaCompilerResult import JavaCompilerResult
from Result import Result
from ProjectEnv import ProjectEnv
import subprocess as sp
from typeAnnotations import *
from isolate import *


class JavaCompiler(Tool):

    """
        Classe d'integration du compilateur Java fondée sur la classe Tool

        Paramètres du constructeur :
            _encoding : type d'encodage
            _classpath : le chemin où sont stockées les librairies supplémentaires 
            _sourcepath : le chemin où trouver les fichiers à compiler
    """

   
    @argumentType("_encoding", str)
    @argumentType("_classpath", str, True)
    @argumentType("command", str)
    def __init__(self, 
                _encoding = "UTF-8",
                _classpath = None,
                command="/usr/bin/javac") :

        Tool.__init__(self, command)
        self.encoding = _encoding
        self.classpath = _classpath


    @argumentType("files", {list : str})
    @argumentType("project_env", ProjectEnv)
    @argumentType("encoding", str, True)
    @argumentType("classpath", str, True)
    @returnType(Result)
    def run(self, project_env,
            files, 
            encoding = None, 
            classpath = None,
            ) :

        """
            Lancement de la compilation de fichiers sources Java

            Paramètres :
                files : liste de String - La liste des fichiers sources a compiler 
        """

        if project_env.is_isolated:
            sourcepath = "./"
        else:
            sourcepath = project_env.student_project_folder + '/' + project_env.sources_path
        classpath = select_arg(classpath, self.classpath)
        #Création de la ligne de commande à partir des arguments
        command_line = [
            self.command, 
            "-encoding", select_arg(encoding, self.encoding),
            "-sourcepath", sourcepath
        ] 
        command_line += (["-cp", classpath] if classpath!= None else [])
        command_line += list(map(lambda f : sourcepath + f,files))
        
        if project_env.is_isolated:
            compilation = isolate_run(project_env.isolate_id, "-p", command_line)
        else:
            compilation = sp.run(command_line, capture_output=True,text=True)
        
        if compilation.stderr != None :
            details = str(compilation.stderr)
        else :
            details = ""
        test_compil = compilation.returncode==0
        result_tool = JavaCompilerResult(files, details, test_compil)
        

        return result_tool

    
    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """
        project_env = ProjectEnv("selfcheck/","./")
        return self.run(["HelloWorld.java"],project_env,sourcepath="./").result=="OK"
    