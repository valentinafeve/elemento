from pattern_reader import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import sys

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = sys.argv[1]
parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)

cont = 1
for line in conll.split('\n'):
    print(f'{cont}:\t{line} ')
    cont+= 1

dg = DependencyGraph(conll)

pr = PatternReader()
matcher = pr.readfromfile('patterns.pt')
i = Inspector( dg.nodes )
m = matcher(i)
