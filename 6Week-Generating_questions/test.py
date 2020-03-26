from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import algorithms as algs

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = "The swamp caterpillar is big and blue"

parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)

cont = 1
for line in conll.split('\n'):
    print(f'{cont}:\t{line} ')
    cont+= 1

dg = DependencyGraph(conll)
plain_tree = algs.generate_tree(dg)
regex = algs.generate_regex('{?*{nsubj*}{cop}*}')
algs.find_patterns(regex, plain_tree)
