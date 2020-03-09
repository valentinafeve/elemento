from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import clean

parser = CoreNLPDependencyParser(url='http://localhost:9000')
for i in range(1,7):
    abreviations="abreviations"
    filename = "text"+str(i)
    f = open("../Fragments_for_testing/"+filename, "r")
    sentences=[]
    for L in f.readlines():
        L=clean.replace(abreviations,L)
        sentences += L.split('.')
    j=1
    for sentence in sentences:
        if len(sentence)>1:
            parse, = parser.raw_parse(sentence)
            conll = parse.to_conll(4)
            dp = DependencyGraph(conll)
            dotted = dp.to_dot()
            graph = dp.nx_graph()
            f = open("outs/"+filename+'_'+str(j)+'.svg', 'w')
            svg = dp._repr_svg_()
            f.write(svg)
            j+=1
