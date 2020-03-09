from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')
for i in range(4,7):

    filename = "text"+str(i)
    f = open("../Fragments_for_testing/"+filename, "r")
    sentences = f.readlines()
    j=1
    for sentence in sentences:
        parse, = parser.raw_parse(sentence)

        conll = parse.to_conll(4)
        dp = DependencyGraph(conll)
        dotted = dp.to_dot()
        graph = dp.nx_graph()
        f = open(filename+'_'+str(j)+'.svg', 'w')
        svg = dp._repr_svg_()
        f.write(svg)
        j+=1
