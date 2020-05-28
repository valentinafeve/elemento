import re
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.dependencygraph import DependencyGraph
from elemento.relations import *
from elemento.time import Time
from elemento.notion import Notion
from elemento.inspector import Inspector

def generate_questions( idee ):

    dictionary = idee.dictionary
    dg = idee.dg
    questions = []
    solved_dictionary = resolve_dictionary( dg, dictionary)
    f = open('elemento/patterns/questions','r+')
    for line in f.readlines():
        words = line.split('=')[0]
        template = line.split('=')[1]
        answer = line.split('=')[2]

        valid_template = True
        for word in words.split(','):
            if not word in list(dictionary.keys()):
                valid_template = False

        if valid_template:
            for k, v in solved_dictionary.items():
                template = template.replace("{"+k+"}",v)
                answer = answer.replace("{"+k+"}",v)
            questions.append({"question": template, "answer": answer})

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
    rels = ['amod','compound','nmod:poss','case','neg','advcl','mark']
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
