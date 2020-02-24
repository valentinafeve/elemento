from nltk.parse import CoreNLPParser
from nltk.tree import Tree

parser = CoreNLPParser(url='http://localhost:9000')
f = open("texts/text2", "r")
sentence = f.read()
list_tree = str(list(parser.parse(sentence.split())))
list_tree = list_tree.replace('Tree','')
list_tree = list_tree.replace('\'','')
list_tree = list_tree.replace(',','')
list_tree = list_tree.replace('[','')
list_tree = list_tree.replace(']','')
list_tree = list_tree.replace('(. .)','')
list_tree = list_tree.replace('(. !)','')
list_tree = list_tree.replace('ROOT','S1')
tree = Tree.fromstring(list_tree)
tree.draw()
