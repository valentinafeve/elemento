import re
from relations import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')

class Notion:
    idees = []

    def __init__(self):
        matchers = []
        f = open("/home/vale/Projects/elemento/elemento/patterns.pt","r+")
        for line in f.readlines():
            matcher = get_matcher(line)
            matchers.append(matcher)
        self.matchers = matchers

    def process_text(self, text):
        sequencial_time = 0
        for sentence in text:
            parse, = parser.raw_parse(sentence)
            conll = parse.to_conll(4)
            dg = DependencyGraph(conll)
            i = Inspector( dg.nodes )
            for matcher in self.matchers:
                idee = matcher(i)
                if not idee.dictionary['WHEN']:
                    idee.time = sequencial_time
                if idee:
                    self.idees.append(idee)
            sequencial_time += 1

    def process_sentence(self, sentence):
        parse, = parser.raw_parse(sentence)
        conll = parse.to_conll(4)
        dg = DependencyGraph(conll)
        i = Inspector( dg.nodes )
        for matcher in self.matchers:
            idee = matcher(i)
            if idee:
                self.idees.append(idee)

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

def get_matcher( line ):
    result = {}
    pattern = line.split(' ')
    wfp = re.findall(r"[\w:']+", pattern[0])
    wfp.reverse()
    wtm = re.findall(r"[\w']+", pattern[1])
    wtm.reverse()

    relations = []
    parent = None

    deep = 0

    pattern[0]+="."
    for c in pattern[0]:
        if c == '{':
            deep+=1
            if deep == 2:
                if not parent:
                    relations.pop()
                    parent = f

            a = wtm.pop()
            b = wfp.pop()

            if b.isupper():
                f = MATCH_TAG(a, b)
            else:
                f = MATCH_REL(a, b)
            if parent:
                f = SON_F(f,1)

            relations.append(f)
        if c == '}':
            deep-=1
            if deep == 0:
                f = relations.pop()
                while relations:
                    f = AND_F(f, relations.pop())
                f = AND_F(parent, f)
                parent = f

            if not relations:
                parent = SON_F(f,-1)

    result = parent
    return result

def generate_questions( dg, dictionary):
    questions = []
    solved_dictionary = resolve_dictionary( dg, dictionary)
    for key, val in dictionary.items():
        if key == "WHO":
            question = key.lower() + ' ' + solved_dictionary["VERB"] + ' ' + solved_dictionary["WHAT"]+'?'
            questions.append({"question": question, "answer": solved_dictionary[key]})
        if key == "WHAT":
            question = key.lower() + ' ' + solved_dictionary["WHO"]+ ' ' + solved_dictionary["VERB"]+'?'
            questions.append({"question": question, "answer": solved_dictionary[key]})
    return questions

def resolve_dictionary( dg, dictionary):
    solved_dictionary = {}
    for key, val in dictionary.items():
        text = smart_resolve_words_from_node( dg, val)
        solved_dictionary[key] = text
    return solved_dictionary

def resolve_words_from_node( dg, node):
    solved_dictionary = {}
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    for child in children:
        text += resolve_words_from_node(dg, child[0])
        text += " "
    text+=dg.nodes.get(node)['word']
    text += " "
    return text

def smart_resolve_words_from_node( dg, node):
    solved_dictionary = {}
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    for child in children:
        done = False
        if not done and dg.nodes.get(child[0])['rel']=='amod':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='compound':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='nmod:poss':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='case':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='neg':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['tag']=='DT':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
    text+=dg.nodes.get(node)['word']
    text += " "
    return text
