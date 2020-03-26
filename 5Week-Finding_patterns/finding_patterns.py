from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import algorithms as algs

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = "The monkey said the lion was dangerous"
sentence = "The elephant told the monkey the lion said he was too dangerous"
sentence = "The women stopped taking the pills because they were carcinogenic."
sentence = "The trophy would not fit in the brown suitcase because it was too big"
sentence = "Marta has a cat, her cat is brown"
parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)

cont = 1
for line in conll.split('\n'):
    print(f'{cont}:\t{line} ')
    cont+= 1

dg = DependencyGraph(conll)
dotted = dg.to_dot()
G = dg.nx_graph()
f = open('test_'+str(datetime.now())+'.svg', 'w')
svg = dg._repr_svg_()
f.write(svg)

how_is_relations = algs.p01(dg)
print('how_is_relations', how_is_relations)
