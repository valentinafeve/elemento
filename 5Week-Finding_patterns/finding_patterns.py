from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import algorithms as algs

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = "Conan and my dog are my friends"
parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)
print(conll)
dg = DependencyGraph(conll)
dotted = dg.to_dot()
G = dg.nx_graph()
f = open('test_'+str(datetime.now())+'.svg', 'w')
svg = dg._repr_svg_()
f.write(svg)

how_is_relations = algs.p01(dg)
print('how_is_relations', how_is_relations)
