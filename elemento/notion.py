import re
from elemento.relations import *
from elemento.time import Time
from elemento.inspector import Inspector
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from colorama import Fore, Style

parser = CoreNLPDependencyParser(url='http://localhost:9000')

def get_words( node, dg, filter=None):
    words = []
    for k, v in dg.nodes.get(node)['deps'].items():
        if filter:
            if not k in filter:
                words.extend(get_words(v[0], dg, filter))
        else:
            words.append(get_words(v[0], dg))
    words.append(dg.nodes.get(node)['word'])
    return words

class Notion:
    idees = []

    def __init__(self,patterns_f=None,time_f=None):
        '''
        patterns_f: path to patterns, must be string
        time_f: path to time, must be string
        '''
        matchers = []
        time_dictionary = {}

        if not patterns_f:
            patterns_f = 'elemento/patterns/idee'

        if not time_f:
            time_f = 'elemento/patterns/time'

        # Reading idee patterns
        f = open(patterns_f,"r+")
        for line in f.readlines():

            result = {}
            pattern = line.split(' ')
            wfp = re.findall(r"[\w:']+", pattern[0])
            wfp.reverse()
            wtm = re.findall(r"[\w']+", pattern[1])
            wtm.reverse()

            relations = []
            parent = None

            deep = 0
            negation = False

            for c in pattern[0]:
                if c == '!':
                    negation = True
                if c == '{':
                    deep+=1
                    if deep == 2:
                        if not parent:
                            relations.pop()
                            parent = f

                    b = wfp.pop()
                    if negation:
                        a = ''
                    else:
                        a = wtm.pop()

                    f = MATCH_TAG(a, b) if b.isupper() else MATCH_REL(a, b)

                    if negation:
                        f = NOT_F(f)
                        negation = False

                    relations.append(f)

                if c == '}':
                    deep-=1
                    if deep == 0:
                        sons = None
                        while relations:
                            f = relations.pop()
                            son = SON_F(f, 1)
                            sons = AND_F(sons, son) if sons else son
                        f = AND_F(parent, sons)
                        parent = SON_F(f,-1)

            result = parent
            matcher = result
            matchers.append(matcher)

        self.matchers = matchers

        # Reading time
        f = open(time_f,"r+")
        for line in f.readlines():
            words = line.split('=')[0].strip()
            time = line.split('=')[1].strip()
            for word in words.split(','):
                time_dictionary[word]=Time(time)
        self.time_dictionary = time_dictionary

    def process_text( self, text, verbose=None):
        sequencial_time = 0
        now = Time()
        for sentence in text:
            if not sentence or sentence[0] == '#':
                continue
            parse, = parser.raw_parse(sentence)
            conll = parse.to_conll(4)
            if verbose:
                cont = 1
                for line in conll.split('\n'):
                    print(f'{cont}:\t{line} ')
                    cont+= 1
            dg = DependencyGraph(conll)
            i = Inspector( dg.nodes )
            for matcher in self.matchers:
                idee = matcher(i)
                if idee:
                    idee.dg = dg
                    if not idee.dictionary.get('WHEN', False):
                        now = now + Time()
                        idee.time = now
                        idee.time.words = "now"
                    else:
                        time_words = get_words(idee.dictionary['WHEN'], idee.dg, filter=['det'])
                        now =  now + Time.get_time( time_words, self.time_dictionary )
                        idee.time = now
                        idee.time.words = time_words
                    self.idees.append(idee)
                    sequencial_time += 1
                    if verbose:
                        print( Fore.GREEN )
                        print('Sentence',sentence)
                        print('Idee',idee)
                        print( Style.RESET_ALL )

    def process_sentence(self, sentence):
        parse, = parser.raw_parse(sentence)
        conll = parse.to_conll(4)
        dg = DependencyGraph(conll)
        i = Inspector( dg.nodes )
        for matcher in self.matchers:
            idee = matcher(i)
            if idee:
                idee.dg = dg
                self.idees.append(idee)
