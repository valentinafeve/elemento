from bllipparser import RerankingParser as rrp
from nltk.parse.api import ParserI
from nltk.tree import Tree
from nltk.data import find

model_dir = find('models/bllip_wsj_no_aux').path
bllip = rrp.from_unified_model_dir(model_dir)

f = open("texts/text2", "r")
sentence = f.read()
all_parses = bllip.parse(sentence)


ptb = all_parses[0].ptb_parse
tree = Tree.fromstring(str(ptb))
tree.draw()
