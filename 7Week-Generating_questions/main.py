from pattern_reader import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
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

pr = PatternReader()
matcher = pr.readfromfile('patterns.pt')
i = Inspector( dg.nodes )
m = matcher(i)

if not m:
    print("There wasn't matches")
else:
    print(m)

# fverb=MATCH_TAG('VERB','VB')
# f0=SON_F(fverb,1)
# fnsubj=MATCH_REL('WHO','nsubj')
# f1=SON_F(fnsubj,1)
# f3=AND_F(f0,f1)
# fnmod=MATCH_REL('WHAT','dobj')
# f2=SON_F(fnmod,1)
# f4=AND_F(f2,f3)
# F=SON_F(f4,-1)
# print( F(i) )
