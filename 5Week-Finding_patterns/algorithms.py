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
                # Recursión ?
    return info

def p01( parse ):
    """
    First pattern. How is X?
    """
    p01_relations = []
    # No es stack porque el sujeto siempre es inmediato.
    nsubj = ''

    conll = parse.to_conll(4)
    dg = DependencyGraph(conll)

    def recursion(node, subtrees):
        sons = dg.nodes[node]['deps'].items()
        for relation, son in sons:
            son = son[0]
            if relation == 'nsubj':
                nsubj = son
            if relation == 'cop':
                # Esto debería ser una clase.
                p01_relations.append(
                    { 'WHO': nsubj, 'VERB': 'IS', 'WHAT': u00(node, parse) }
                )
            recursion(son, sons)
        return p01_relations

    # All subtrees that matches the pattern
    sons = dg.nodes[0]['deps'].items()
    return recursion(0, sons)
