import random
def generate_questions( dg, dictionary):
    questions = []
    solved_dictionary = resolve_dictionary( dg, dictionary)
    for key, val in dictionary.items():
        # if (key != "WHO") and (key != "VERB") and solved_dictionary["WHO"] and solved_dictionary["VERB"]:
        #     question = key.lower() + " " + solved_dictionary["WHO"] + solved_dictionary["VERB"]+'?'
        #     questions.append({"question": question, "answer": solved_dictionary[key]})
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
    for child in children:
        if dg.nodes.get(child[0])['rel']=='amod':
            text += smart_resolve_words_from_node(dg, child[0])
            text += " "
    text+=dg.nodes.get(node)['word']
    text += " "
    return text
