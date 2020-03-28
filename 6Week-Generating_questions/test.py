from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import algorithms as algs
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
G = dg.nx_graph()
filename = sentence.replace(' ','_')
f = open(filename+str(datetime.now())+'.svg', 'w')
svg = dg._repr_svg_()
f.write(svg)

plain_tree = algs.generate_tree(dg)

f = open("patterns.pt", "r")
for line in f.readlines():
    pattern = line.split(' ')[0]
    destin = line.split(' ')[1]
    sentence = sys.argv[1]
    regex = algs.generate_regex( pattern )
    print('regex',regex)
    print('tree',plain_tree)

    match = algs.match_patterns( regex, plain_tree)
    if match:
        pattern_stack = algs.generate_pattern_stack(pattern)
        evaluating_stack = algs.generate_evaluating_stack(match)
        destin_stack = algs.generate_destin_stack(destin.rstrip())
        dictionary = algs.generate_dictionary(pattern_stack, evaluating_stack, destin_stack)
        print(dictionary)
