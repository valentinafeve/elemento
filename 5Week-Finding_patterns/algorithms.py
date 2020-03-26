from nltk.parse.dependencygraph import DependencyGraph
def u00( node, parse ):
    """
    Get aditional information about a node.
    """
    # https://universaldependencies.org/tagset-conversion/en-penn-uposf.html
    conll = parse.to_conll(4)
    dg = DependencyGraph(conll)
    info = {}
    sons = dg.nodes[node]['deps'].items()
    tag = parse.nodes[node]['ctag']
    print(tag)

    if tag == 'NN':
        info['NOUN'] = node
    if tag == 'NNP':
        # propn
        info['NOUN'] = node
    if tag == 'NNPS':
        # propn plural
        info['NOUN'] = node
    if tag == 'NNS':
        # plural
        info['NOUN'] = node
    if tag == 'JJ':
        info['ADJ'] = node

    if tag == 'NN' or tag == 'NNPS' or tag == 'NNS':
        for relation, son in sons:
            if relation == 'amod':
                tag = parse.nodes[son[0]]['ctag']
                if tag == 'JJ':
                    info['ADJ'] = son[0]
                if tag == 'JJR':
                    # Comparativo
                    info['ADJ'] = son[0]
                if tag == 'JJS':
                    # Superlativo
                    info['ADJ'] = son[0]
                if tag == 'CC':
                    print(1)
                    # Recursión ?
    return info

def u01( stack, parse ):
    # TO-DO: Determinar el sujeto
    return stack

def p01( parse ):
    """
    First pattern. How is X?
    """

    # Relaciones tipo p01
    p01_relations = []

    # Lista de sujetos
    nsubj = []

    dg = DependencyGraph(parse.to_conll(4))

    def recursion(node, subtrees):
        sons = dg.nodes[node]['deps'].items()
        for relation, son in sons:
            son = son[0]
            if relation == 'nsubj':
                tag = parse.nodes[son]['ctag']
                if not tag == 'PRP':
                    nsubj.append(son)
            if relation == 'dobj':
                tag = parse.nodes[son]['ctag']
                nsubj.append(son)
            if relation == 'cop':
                # Esto debería ser una clase.

                p01_relations.append(
                    { 'WHO': nsubj, 'VERB': 'IS', 'WHAT': node }
                )
            recursion(son, sons)
        return p01_relations

    # All subtrees that matches the pattern
    sons = dg.nodes[0]['deps'].items()
    return recursion(0, sons)
