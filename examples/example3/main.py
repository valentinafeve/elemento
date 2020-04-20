from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from datetime import datetime
import sys
from colorama import Fore, Style
import sys
sys.path.insert(1, '../../elemento')
import elemento as el

parser = CoreNLPDependencyParser(url='http://localhost:9000')

# List of dictionaries
dictionaries = []

# List of functions known as matchers
matchers = []

# List of dictionaries of questions { question, answer}
questions = []

# Reading matchers from patterns file
f = open("../patterns.pt","r+")
for line in f.readlines():
    matcher = el.get_matcher(line)
    matchers.append(matcher)

# Reading sentences from book
f = open("../books/The_pirate_Modi.txt","r+")

# Getting dictionaries from array of sentences
dictionaries = el.get_dictionaries_from_text( f.readlines(), matchers, verbose=True )
