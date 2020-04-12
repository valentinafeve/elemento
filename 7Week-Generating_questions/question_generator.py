def generate_question( dg, dictionary):
    solved_dictionary = {}
    for key, val in dictionary.items():
        text = resolve_words_from_node( dg, val)
        solved_dictionary[key] = text
    return solved_dictionary

def resolve_words_from_node( dg, node):
    print("Resolving from node",node)
    solved_dictionary = {}
    children = dg.nodes.get(node)['deps'].values()
    print(children)
    text = ""
    for child in children:
        text += resolve_words_from_node(dg, child[0])
        text += " "
    text+=dg.nodes.get(node)['word']
    text += " "
    print(text)
    return text
