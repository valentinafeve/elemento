from pattern_reader import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import sys
from colorama import Fore, Style

parser = CoreNLPDependencyParser(url='http://localhost:9000')

dictionaries = []

f = open("sentences","r+")
for sentence in f.readlines():
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
            dictionaries.append(m)
            print("Line:",index)
            print("Sentence:",sentence)
            print( Fore.BLUE + str(m))
            print( Style.RESET_ALL )
        index+= 1

print( Fore.BLUE )
print("DICTIONARIES:")
for dictionay in dictionaries:
    print(dictionay)
print( Style.RESET_ALL )
