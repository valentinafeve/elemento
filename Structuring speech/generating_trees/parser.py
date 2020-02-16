from nltk.data import find

from nltk.parse.api import ParserI
from nltk.tree import Tree
from bllipparser import RerankingParser as rrp

model_dir = find('models/bllip_wsj_no_aux').path
bllip = rrp.from_unified_model_dir(model_dir)

sentence = 'British left waffles on Falklands .'.split()
all_parses = bllip.parse(sentence)
print(type(all_parses[0]))
