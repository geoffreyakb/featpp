
from Tool import Tool
from JavaCompilerResult import JavaCompilerResult
import subprocess as sp



class Junit(Tool):

    """
        Classe d'integration de JUnit fondée sur la classe Tool
    """

    def run(self, files, options):

        """
            Lancement de la compilation d'un ou plusieurs fichiers sources Java

            java -cp junit.jar;. junit.textui.TestRunner MaClasseTest
            Paramètres :
                files : liste de String - La liste des fichiers sources a compiler
                options : liste de String - La liste des options de compilation   
        """

            
        command = ['java','-cp', self.input, ';.'] + list(options) \
                + [] \
                + ['-d', self.output] \
                + [files[0]]
                    
        compilation = sp.run(command, capture_output=True,text=True)
        details = str(compilation.stderr)
        test_compil = compilation.returncode==0
        result_tool = JavaCompilerResult(_file, details, test_compil)
        

        return result_tool
    
   
    def selfcheck(self):

        """
            Lancement d'un test rapide de compilation sur un hello world ecrit en Java
        """

        return self.run([os.path.abspath(HelloWorld.java)], [])