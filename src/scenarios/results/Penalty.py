from Result import * 
from typeAnnotations import *

class Penalty(Result) :

    @argumentType("_msg", str)
    @argumentType("_penalty", int)
    def __init__(self, _msg, _penalty) :
        Result.__init__(self, FAILURE)
        self.msg = _msg
        self.penalty = _penalty

    @argumentType("mode", int)
    @returnType(str)
    def get_message(self, mode=0):
        return self.msg + '\n'