from elemento import pronoun_finder as pnf
from elemento.relations import *
import elemento.relations as rel
from elemento.inspector import Inspector
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import gensim.downloader as api
import gensim
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
    def __init__(self,patterns_f=None,time_f=None,model=None):
        '''
        patterns_f: path to patterns, must be string
        time_f: path to time, must be string
        '''
        self.matchers = []
        self.idees = []
        self.time_dictionary = {}
        self.model: gensim.models.keyedvectors.Word2VecKeyedVectors = model
        self.nouns = {}
        # if not model:
            # self.model = api.load("glove-wiki-gigaword-300")
        if not patterns_f:
            patterns_f = 'elemento/patterns/idee'
        if not time_f:
            time_f = 'elemento/patterns/time'

        # Reading idee patterns
        file = open(patterns_f,"r+")
        for line in file.readlines():
            if line[0] == "#":
                continue

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
            self.matchers.append(matcher)
        file.close()

    def process_sentence(self, sentence, verbose=False, solve_pronouns=False):
        try:
            parse, = parser.raw_parse(sentence)
            conll = parse.to_conll(4)
            if verbose:
                cont = 1
                print(Fore.YELLOW)
                for line in conll.split('\n'):
                    print(f'{cont}:\t{line} ')
                    cont+= 1
                print('\n')
                print(Style.RESET_ALL)
        except Exception:
            ## TODO: Raise exception
            return
        dg = DependencyGraph(conll)
        i = Inspector(dg.nodes)
        solved_pronouns = None
        if solve_pronouns:
            f = rel.ALL_F(
                    rel.AND_F(
                        rel.MATCH_TAG('noun', 'NN'),
                        rel.MATCH_REL('noun', 'nsubj'),
                    )
                )
            noun_list = f(i)
            if noun_list:
                node = noun_list[0].get('noun')
                n = dg.nodes.get(node)['word'].lower()
                current = self.nouns.get(n, 0)
                self.nouns[n] = current+1
            nouns = sorted(self.nouns.items(), key=lambda x: x[1], reverse=True)
            popular_noun, score = nouns[0]
            solved_pronouns = pnf.resolve_pronouns(inspector=i, model=self.model, default_noun=popular_noun)
        for matcher in self.matchers:
            idee = matcher(i)
            if idee:
                idee.solved_pronouns = solved_pronouns
                idee.dg = dg
                if verbose:
                    print(Fore.MAGENTA)
                    print(idee)
                    if idee.solved_pronouns:
                        print(idee.solved_pronouns)
                    print(Style.RESET_ALL)
                    print('\n')
                self.idees.append(idee)

    def process_text( self, text, verbose=False, solve_pronouns=False):
        for sentence in text:
            if not sentence or sentence[0] == '#':
                continue
            self.process_sentence(sentence, verbose=verbose, solve_pronouns=solve_pronouns)
