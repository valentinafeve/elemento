from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph

parser = CoreNLPDependencyParser(url='http://localhost:9000')

sentence = "The trophy would not fit in the brown suitcase because it was too big"
# sentence = "I spread the roth on the table in order to protect it"
# sentence = "On the table I've spread the roth in order to protect it"
# sentence = "The city councilmen refused the demonstrators a permit because they feared violence"
# sentence = "She said he told her their secrets"
sentence = "The monkey said the bird told the elephant he was dangerous."
sentence = "The women stopped taking the pills because they were carcinogenic."
sentence = "Marta has a cat, her cat is brown"
parse, = parser.raw_parse(sentence)
conll = parse.to_conll(4)
print(conll)
dg = DependencyGraph(conll)
dotted = dg.to_dot()
G = dg.nx_graph()
f = open('hoy_'+str(datetime.now())+'.svg', 'w')
svg = dg._repr_svg_()
f.write(svg)
