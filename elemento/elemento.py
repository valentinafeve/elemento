from elemento.relations import *
import gensim.downloader as api
import numpy as np
from elemento.relations import *
from elemento.time import Time
from elemento.notion import Notion
from elemento.inspector import Inspector
import nltk
from nltk.corpus import stopwords
import elemento.pronoun_finder

exceptions = ['how', 'who', 'what', 'when', 'where', 'is', 'was', 'were']

def generate_questions(idee):
    dictionary = idee.dictionary
    dg = idee.dg
    questions = []
    solved_dictionary = resolve_dictionary(dg, dictionary)
    f = open('elemento/patterns/questions', 'r+')
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
                template = template.replace("{" + k + "}", v)
                answer = answer.replace("{" + k + "}", v)
            questions.append({"question": template, "answer": answer})

    return questions


def resolve_dictionary(dg, dictionary):
    solved_dictionary = {}
    for key, val in dictionary.items():
        text = smart_resolve_words_from_node(dg, val)
        solved_dictionary[key] = text
    return solved_dictionary


def resolve_dictionary_wv(idee: Idee, solved_pronouns=None, model=None):
    if not model:
        model = api.load("glove-wiki-gigaword-50")
    dg = idee.dg
    dictionary = idee.dictionary
    solved_dictionary = {}
    for key, val in dictionary.items():
        rels = ['compound','nmod','case','amod','conj']
        text = smart_resolve_words_from_node(dg, val, rels=rels, solved_pronouns=solved_pronouns).lower()
        vectors = []
        for word in text.split():
            if word and (word in exceptions or word not in stopwords.words('english')):
                try:
                    word_vector = model.wv.get_vector(word)
                    vectors.append(word_vector)
                except:
                    pass
        if vectors:
            vector = np.average(vectors, axis=0)
            solved_dictionary[key] = vector
    return solved_dictionary


def resolve_words_from_node(dg, node, solved_pronouns=None):
    if solved_pronouns:
        if node in solved_pronouns:
            node = solved_pronouns[node]
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    for child in children:
        text += resolve_words_from_node(dg, child[0])
        text += " "
    text += dg.nodes.get(node)['word']
    text += " "
    return text


def smart_resolve_words_from_node(dg, node, rels=None, solved_pronouns=None):
    if solved_pronouns:
        if node in solved_pronouns:
            node = solved_pronouns[node]
    children = dg.nodes.get(node)['deps'].values()
    text = ""
    if not rels:
        rels = ['amod', 'compound', 'nmod:poss', 'case', 'neg', 'advcl', 'mark', 'obl', 'det']
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
    text += dg.nodes.get(node)['word']
    text += " "
    return text
