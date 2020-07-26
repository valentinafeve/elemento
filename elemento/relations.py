import inspect
import re
import gensim.downloader as gensim

# model=gensim.load("glove-twitter-25")

class Idee:
    def __init__(self, dictionary=None):
        if dictionary is None:
            dictionary = {}
        self.time = 0
        self.dg = None
        self.dictionary = dictionary
        self.weight=0
        self.solved_pronouns = {}

    def __repr__(self):
        return '<Dictionary: '+str(self.dictionary)+'>'

    def __str__(self):
        return str(self.dictionary)

    def __bool__(self):
        return True if self.dictionary else False

    # def get_weight(self):
    #     words=self.get_words()
    #     words=[words[k] for k in words if words[k] in model]
    #     self.weight=model.n_similarity(words[0],words)
    #     return self.weight

    def get(self, key):
        return self.dictionary.get(key, False)

    def keys(self):
        return self.dictionary.keys()

    def values(self):
        return self.dictionary.values()

    def set_data(self, relation, data):
        self.dictionary[relation] = data

    def update(self, idee):
        self.dictionary.update(idee.dictionary)

    def get_words(self):
        R={}
        for k in self.dictionary:
            R[k]=self.dg.nodes[self.dictionary[k]]['word']
        return R

def any(tree):
    return Idee()

def NOT_F(f):
    def not_f(tree):
        return None if f(tree) else Idee(dictionary={'NOT': tree.get_state()})
    return not_f

def OR_F(*args):
    F=[]
    default=None
    for f in args:
        if callable(f):
            if f!=any:
                F+=[f]
            else:
                default=Idee()
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
        R=Idee()
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
            idee = Idee()
            idee.set_data(match,tree.get_state())
            return idee
    return match_tag


def MATCH_REL(match,rel):
    def match_rel(tree):
        if re.match(rel,tree.get_rel()):
            idee = Idee()
            idee.set_data(match,tree.get_state())
            return idee
    return match_rel

'''
operators:
     -> AND_F(fA,SON_F(B,1))
    exp2=A;B -> AND_F(fA,fB)
    exp3=A|B -> OR_F(fA,fB)
    exp4=key<tag>[rel] -> AND_F(MATCH_TAG(key,tag),MATCH_REL(key,rel))
'''
