import inspect
from tree_generator import parse
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
        if self.state==0:
            return 'None'
        return self.nodes[self.state]['rel']

    def get_lemma(self):
        return self.nodes[self.state]['lemma']

    def get_state(self):
        return self.state


def any(tree):
    return {}

def OR_F(*args):
    F=[]
    default=None
    for f in args:
        if callable(f):
            if f!=any:
                F+=[f]
            else:
                default={}
    def or_f(tree):
        for f in F:
            r=f(tree)
            if r:
                return r
        return default
    return or_f

def AND_F(*args):
    F=[f for f in args if callable(f) and f!=any]
    def and_f(tree):
        R={}
        for f in F:
            r=f(tree)
            if not r:
                return None
            R.update(r)
        return R
    return and_f

def SON_F(f,n=1):
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

def ALL_F(f):
    def all_f(tree):
        R=[]
        for c in tree.children():
            R+= all_f(c)
        r=f(tree)
        R+= [r] if r is not None else []
        return R
    return all_f

def MATCH_TAG(match,tag):
    def match_tag(tree):
        if re.match(tag,tree.get_tag()):
            return {match:tree.get_state()}
    return match_tag


def MATCH_REL(match,rel):
    def match_rel(tree):
        if re.match(rel,tree.get_rel()):
            return {match:tree.get_state()}
    return match_rel

'''
operators:
     -> AND_F(fA,SON_F(B,1))
    exp2=A;B -> AND_F(fA,fB)
    exp3=A|B -> OR_F(fA,fB)
    exp4=key<tag>[rel] -> AND_F(MATCH_TAG(key,tag),MATCH_REL(key,rel))
'''

F={}

F['WHO_VERB_WHAT']=ALL_F(OR_F(
    AND_F(#form x is y
        MATCH_TAG('VERB','VB'),
        SON_F(MATCH_REL('WHO','nsubj')),
        SON_F(OR_F(MATCH_REL('WHAT','dobj|nmod'),any))
    ),
    AND_F(
        MATCH_TAG('WHAT','.*'),
        SON_F(MATCH_REL('WHO','nsubj')),
        SON_F(MATCH_REL('VERB','cop'))
    )
))

def find_paterns(sentence,file=None):
    ins=Inspector(parse(sentence,file).nodes)
    R=[]
    for f in F.values():
        R+=[f(ins)]
    return R
