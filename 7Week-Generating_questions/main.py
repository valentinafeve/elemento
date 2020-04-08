from pattern_reader import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from colorama import Fore, Style
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
matchers = pr.readfromfile('patterns.pt')
index = 1
for matcher in matchers:
    i = Inspector( dg.nodes )
    m = matcher(i)
    if not m:
        print("There wasn't matches with pattern %d" % index)
    else:
        print( Fore.BLUE + str(m))
        print( Style.RESET_ALL )
    index+= 1
