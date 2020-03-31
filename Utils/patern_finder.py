import inspect 
import re
"""
    input tree
"""

class Inspector():
    def __init__(self,nds,st=0):
        self.nodes=nds
        self.state=st

    def children(self):
        R=[]
        deps=self.nodes[self.state]['deps']
        for r in deps:
            R+=[Inspector(self.nodes,deps[r][0])]
        return R

    def get_tag(self):
        return self.nodes[self.state]['tag']
    
    def get_rel(self):
        return self.nodes[self.state]['rel']

    def get_lemma(self):
        return self.nodes[self.state]['lemma']


def OR_F(f1,f2):
    sig1=inspect.signature(f1)
    sig2=inspect.signature(f2)
    if(sig1!=sig2):
        raise Exception('functions must have the same signature')
    S=str(sig1)[1:-1]
    rfunct="lambda %s: f1(%s) or f2(%s)"%(S,S,S)
    return eval(rfunct,{'f1':f1,'f2':f2},None)

def AND_F(f1,f2):
    def and_value(dic1,dic2):
        if dic1 and dic2:
            dic1.update(dic2)
            return dic1
        else:
            return None
    sig1=inspect.signature(f1)
    sig2=inspect.signature(f2)
    if(sig1!=sig2):
        raise Exception('functions must have the same signature')
    S=str(sig1)[1:-1]
    rfunct="lambda %s: and_value(f1(%s),f2(%s))"%(S,S,S)
    return eval(rfunct,{'f1':f1,'f2':f2,'and_value':and_value},None)

def SON_F(f,n):
    """
        f must take something with the method childs()
        n is the depth on wich f is satisfied, -1 for any depth 
    """
    
    def son_f_rec(tree,n):
        if n==0:
            return None
        children=tree.children()
        if len(children)==0:
            return None
        for C in children:
            r=f(C)
            if r:
                return r
        for C in children:
            r=son_f(C)
            if r:
                return son_f_rec(C,n-1)
        return None

    def son_f(tree):
        return son_f_rec(tree,n)

    rfunct="lambda %s:{}"
    return son_f

def MATCH_TAG(match,tag):
    n=len(tag)
    def match_tag(tree):
        if tree.get_tag()[:n]==tag:
            return {match:tree.get_lemma()}
    return match_tag


def MATCH_REL(match,rel):
    n=len(rel)
    def match_rel(tree):
        if tree.get_rel()[:n]==rel:
            return {match:tree.get_lemma()}
    return match_rel


fnsubj=MATCH_REL('WHO','nsubj')
fnmod=MATCH_REL('WHAT','dobj')
fverb=MATCH_TAG('VERB','VB')
f1=SON_F(fnsubj,1)
f2=SON_F(fnmod,1)
f3=AND_F(f1,f2)
f4=AND_F(fverb,f3)
F=SON_F(f4,-1)