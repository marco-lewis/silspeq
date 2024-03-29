from lark.visitors import *
from lark import Token
from z3 import *

class SilSpeqZ3FlagVisitor(Visitor):
    oracles = []
    quantum_out = False
    meas_rand = False
    meas_cert = False
    meas_whp = -1
    meas_atval = False
    
    def __init__(self):
        super().__init__()
    
    def specs(self, specs):
        pass
    
    def funcspec(self, tree):
        pass
    
    def qout(self, v):
        self.quantum_out = True
        
    def rand(self, v):
        self.meas_rand = True

    def cert(self, v):
        self.meas_cert = True

    def whp(self, v):
        self.meas_whp = 0.5

    def whpvalue(self, v:Tree):
        if list(v.find_data('pdec')): d = self.pdec(v.children[0])
        elif list(v.find_data('pdiv')): d = self.pdiv(v.children[0])
        self.meas_whp = d

    def pdec(self, v:Tree):
        return float("0." + str(self.token(v.children[0])))

    def pdiv(self, v:Tree):
        children = v.children
        ints = [self.token(c) for c in children]
        return ints[0] / ints[1]

    def atvalue(self, v: Tree):
        dtree = list(v.find_data('definition'))[0]
        mark = self.definition(dtree)
        self.meas_atval = mark

    def oracle(self, v):
        return lambda name: self.oracles.append(name)

    def definition(self, v:Tree):
        name = self.token(v.children[0])
        return Int(name)

    def token(self, tok: Token):
        if tok.type == "INT": return self.INT(tok)
        if tok.type == "NUMBER": return self.NUMBER(tok)
        if tok.type == "NAME": return self.NAME(tok)

    def INT(self, n: Token):
        return int(n.value)

    def NUMBER(self, n):
        return float(n.value)

    def NAME(self, var):
        return var.value
