import re
from relations import *
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from datetime import datetime
import sys
from colorama import Fore, Style

sys.path.insert(1, '../../elemento')
parser = CoreNLPDependencyParser(url='http://localhost:9000')

def get_inspector( dg ):
    return Inspector(dg.nodes)

def get_matcher( line ):
    result = {}
    pattern = line.split(' ')
    wfp = re.findall(r"[\w?']+", pattern[0])
    wfp.reverse()
    wtm = re.findall(r"[\w']+", pattern[1])
    wtm.reverse()

    relations = []
    parent = None

    deep = 0

    pattern[0]+="."
    for c in pattern[0]:
        if c == '{':
            deep+=1
            if deep == 2:
                if not parent:
                    relations.pop()
                    parent = f

            a = wtm.pop()
            b = wfp.pop()

            if b.isupper():
                f = MATCH_TAG(a, b)
            else:
                f = MATCH_REL(a, b)
            if parent:
                f = SON_F(f,1)

            relations.append(f)
        if c == '}':
            deep-=1
            if deep == 0:
                f = relations.pop()
                while relations:
                    f = AND_F(f, relations.pop())
                f = AND_F(parent, f)
                parent = f

            if not relations:
                parent = SON_F(f,-1)

    result = parent
    return result

def generate_questions( dg, dictionary):
    questions = []
    solved_dictionary = resolve_dictionary( dg, dictionary)
    for key, val in dictionary.items():
        if key == "WHO":
            question = key.lower() + ' ' + solved_dictionary["VERB"] + ' ' + solved_dictionary["WHAT"]+'?'
            questions.append({"question": question, "answer": solved_dictionary[key]})
        if key == "WHAT":
            question = key.lower() + ' ' + solved_dictionary["WHO"]+ ' ' + solved_dictionary["VERB"]+'?'
            questions.append({"question": question, "answer": solved_dictionary[key]})
    return questions

def resolve_dictionary( dg, dictionary):
    solved_dictionary = {}
    for key, val in dictionary.items():
        text = smart_resolve_words_from_node( dg, val )
        solved_dictionary[key] = text
    return solved_dictionary

def resolve_words_from_node( dg, node):
    solved_dictionary = {}
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    for child in children:
        text += resolve_words_from_node(dg, child[0])
        text += " "
    text+=dg.nodes.get(node)['word']
    text += " "
    return text

def smart_resolve_words_from_node( dg, node):
    solved_dictionary = {}
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    for child in children:
        done = False
        if not done and dg.nodes.get(child[0])['rel']=='amod':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='compound':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='nmod:poss':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='case':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['rel']=='neg':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['tag']=='DT':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
    text+=dg.nodes.get(node)['word']
    text += " "
    return text

def get_dictionaries_from_text( text, matchers, verbose=None ):
    dictionaries = []
    for sentence in text:
        if verbose:
            print( Fore.MAGENTA + str(sentence))
            print( Style.RESET_ALL )
        if sentence[0] == "#":
            continue

        # Parsing from Stanford
        parse, = parser.raw_parse(sentence)
        conll = parse.to_conll(4)
        if verbose:
            print(conll)
        dg = DependencyGraph(conll)

        for m in matchers:
            i = get_inspector(dg)
            dictionary = m(i)
            if dictionary:
                dictionaries.append( dictionary )
                if verbose:
                    print( Fore.BLUE + str(dictionary))
                    print( Style.RESET_ALL )
    if verbose:
        print( Fore.BLUE )
        print("DICTIONARIES:")
        for dictionary in dictionaries:
            print(dictionary)
        print( Style.RESET_ALL )
    return dictionaries
