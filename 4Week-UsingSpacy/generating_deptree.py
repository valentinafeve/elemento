from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')

filename = "text6"
f = open("../Fragments_for_testing/"+filename, "r")
sentences = f.readlines()
for sentence in sentences:
    parse, = parser.raw_parse(sentence)

    conll = parse.to_conll(4)
    dp = DependencyGraph(conll)
    dotted = dp.to_dot()
    graph = dp.nx_graph()
    f = open(filename+'_'+str(datetime.now())+'.svg', 'w')
    svg = dp._repr_svg_()
    f.write(svg)
