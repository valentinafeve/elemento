import re
def generate_tree( dg ):
    """
    Generating string tree like {root{{son}{son2}}}
    """

    def recursion(node, relation):
        sons = dg.nodes[node]['deps'].items()
        st = ""
        for son_relation, son in sons:
            son = son[0]
            st+='{%s}' %recursion(son, son_relation)
        fst = "%s:%s%s" % (str(node), relation, st)
        return fst

    # All subtrees that matches the pattern
    return "{%s}" % recursion(0, '')

def generate_regex( pattern ):
    matches = re.findall(r"[a-z]+\w", pattern)
    pattern = pattern.replace('?','([0-9]+:[a-zA-Z]+)')
    pattern = pattern.replace('*','({[0-9]+:[a-zA-Z]+({.*?})*})*')
    for match in matches:
        pattern = pattern.replace(match, '[0-9]+:'+match)
    return pattern

def find_patterns( regex, dictionary_destin ):
    print(regex)
    print(dictionary_destin)
