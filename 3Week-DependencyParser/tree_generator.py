from datetime import datetime
from nltk.parse.corenlp import CoreNLPDependencyParser
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')


sentence = "the cat ran in the house"
parse, = dep_parser.raw_parse(sentence)

f = open(str(datetime.now())+'.svg', 'w')
svg = parse._repr_svg_()
f.write(svg)

print(parse.to_conll(4))
