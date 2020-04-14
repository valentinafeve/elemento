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
index_line = 0

for sentence in f.readlines():
    index_line+=1
    if sentence[0] == "#":
        continue

    # Parsing from Stanford
    parse, = parser.raw_parse(sentence)
    conll = parse.to_conll(4)
    dg = DependencyGraph(conll)

    # Generate tree as svg
    if len(sys.argv)==2:
        f = open('svg_'+str(index_line)+'.svg', 'w')
        svg = parse._repr_svg_()
        f.write(svg)
        f.close()

    # Printing conll
    cont = 1
    for line in conll.split('\n'):
        print(f'{cont}:\t{line} ')
        cont+= 1

    index = 1
    print( Fore.GREEN )
    print("Line:",index)
    print("Sentence:",sentence)
    print( Style.RESET_ALL )

    # Trying sentence with all the matchers
    for matcher in matchers:
        i = el.get_inspector( dg )
        dictionary = matcher(i)
        if not dictionary:
            print("There wasn't matches with pattern %d" % index)
        else:
            dictionaries.append(dictionary)
            print( Fore.BLUE + str(dictionary))
            print( Style.RESET_ALL )
            questions.extend( el.generate_questions( dg, dictionary))
        index+= 1

print( Fore.BLUE )
print("DICTIONARIES:")
for dictionay in dictionaries:
    print(dictionay)
print( Style.RESET_ALL )

print( Fore.RED)
print("QUESTIONS:")
for question in questions:
    print("Question:", question["question"])
    print("Answer:", question["answer"])
    print("\n")
print( Style.RESET_ALL )
