import re
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
import random
import re
from elemento.relations import *
from elemento.time import Time
from elemento.notion import Notion
from elemento.inspector import Inspector

def generate_questions( idee ):
    dictionary = idee.dictionary
    dg = idee.dg
    questions = []
    solved_dictionary = resolve_dictionary( dg, dictionary)
    for key, val in dictionary.items():
        if key == "WHO":
            if solved_dictionary.get("WHAT", False):
                question = key.lower() + ' ' + solved_dictionary["VERB"] + ' ' + solved_dictionary["WHAT"]+'?'
                questions.append({"question": question, "answer": solved_dictionary[key]})
            else:
                question = key.lower() + ' ' + solved_dictionary["VERB"] +'?'
                questions.append({"question": question, "answer": solved_dictionary[key]})
        if key == "WHAT":
            if solved_dictionary.get("MARK", False):
                question = key.lower() + ' ' + solved_dictionary["WHO"]+ ' ' + solved_dictionary["VERB"]+solved_dictionary["MARK"]+'?'
            else:
                question = key.lower() + ' ' + solved_dictionary["WHO"]+ ' ' + solved_dictionary["VERB"]+'?'
            questions.append({"question": question, "answer": solved_dictionary[key]})
        if key == "WHEN":
            if solved_dictionary.get("WHO", False) and solved_dictionary.get("VERB", False) and solved_dictionary.get("WHAT", False):
                question = key.lower() + ' ' + solved_dictionary["WHO"] + ' ' + solved_dictionary["VERB"] + solved_dictionary["WHAT"]
                words = idee.time.words
                words_str = ' '.join([str(word)+' ' for word in words])
                questions.append({"question": question, "answer": words_str })
            else:
                if solved_dictionary.get("WHO", False) and solved_dictionary.get("VERB", False):
                    question = key.lower() + ' ' + solved_dictionary["WHO"] + ' ' + solved_dictionary["VERB"]
                    words = idee.time.words
                    words_str = ' '.join([str(word)+' ' for word in words])
                    questions.append({"question": question, "answer": words_str })
    return questions

def resolve_dictionary( dg, dictionary):
    solved_dictionary = {}
    for key, val in dictionary.items():
        text = smart_resolve_words_from_node( dg, val)
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
    rels = ['amod','compund','nmod:poss','case','neg']
    tags = ['DT']
    for child in children:
        done = False
        if not done and dg.nodes.get(child[0])['rel'] in rels:
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
        if not done and dg.nodes.get(child[0])['tag'] in tags:
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
            done = True
    text+=dg.nodes.get(node)['word']
    text += " "
    return text
