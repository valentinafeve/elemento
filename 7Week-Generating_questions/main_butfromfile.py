from pattern_reader import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from datetime import datetime
from question_generator import *

import sys
from colorama import Fore, Style

parser = CoreNLPDependencyParser(url='http://localhost:9000')

dictionaries = []

pr = PatternReader()
matchers = pr.readfromfile('patterns.pt')
questions=[]
f = open("sentences","r+")
index_line = 0
for sentence in f.readlines():
    index_line+=1
    if sentence[0] == "#":
        continue

    # Parse
    parse, = parser.raw_parse(sentence)
    conll = parse.to_conll(4)
    dg = DependencyGraph(conll)

    # Generate tree as svg
    if len(sys.argv)==2:
        f = open('svg_'+str(index_line)+'.svg', 'w')
        svg = parse._repr_svg_()
        f.write(svg)
        f.close()

    # Printing conll
    cont = 1
    for line in conll.split('\n'):
        print(f'{cont}:\t{line} ')
        cont+= 1


    index = 1
    print( Fore.GREEN )
    print("Line:",index)
    print("Sentence:",sentence)
    print( Style.RESET_ALL )
    for matcher in matchers:
        i = Inspector( dg.nodes )
        m = matcher(i)
        if not m:
            print("There wasn't matches with pattern %d" % index)
        else:
            dictionaries.append(m)
            print( Fore.BLUE + str(m))
            print( Style.RESET_ALL )
            questions.extend(generate_questions( dg, m))
        index+= 1

print( Fore.BLUE )
print("DICTIONARIES:")
for dictionay in dictionaries:
    print(dictionay)
print( Style.RESET_ALL )

print( Fore.RED)
print("QUESTIONS:")
print(questions)
print( Style.RESET_ALL )
