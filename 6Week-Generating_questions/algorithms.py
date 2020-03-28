import re

def generate_pattern_stack(string1):
    """
    Generate the stack for a string like '{?*{nsubj}{cop}*}'
    """
    i1 = 0
    i2 = 0
    level1 = -1
    level2 = -1
    to_found = []
    while i1 < len(string1):
        if string1[i1] == '{':
            i1 +=1
            level1+=1
            continue
        if string1[i1] == '}':
            i1 +=1
            level1-=1
            continue
        if string1[i1] == '?':
            to_found.append({'level':level1, 'match':'?'})
            i1 += 1
            continue
        if string1[i1] == '*':
            to_found.append({'level':level1, 'match':'*'})
            i1 += 1
            continue
        if re.search('[a-zA-Z:]', string1[i1]):
            temp = ''
            while re.search('[a-zA-Z:]', string1[i1]):
                temp+=string1[i1]
                i1+=1
            to_found.append({'level':level1,'match':temp})
            continue
    return to_found

def generate_evaluating_stack(string2):
    """
    Generate the stack for a string like '{5:ROOT{3:nsubj{1:det}{2:amod}}{4:cop}{6:cc}{7:conj}}'
    """
    i1 = 0
    level1 = -1
    to_found = []
    while i1 < len(string2):
        if string2[i1] == '{':
            i1 +=1
            level1+=1
            continue
        if string2[i1] == '}':
            i1 +=1
            level1-=1
            continue
        if string2[i1] == '?':
            to_found.append({'level':level1, 'match':'?'})
            i1 += 1
            continue
        if string2[i1] == '*':
            to_found.append({'level':level1, 'match':'*'})
            i1 += 1
            continue
        if re.search('[a-zA-Z0-9:]', string2[i1]):
            temp = ''
            while re.search('[a-zA-Z0-9:]', string2[i1]):
                temp+=string2[i1]
                i1+=1
            to_found.append({'level':level1,'match':temp})
            continue
    return to_found

def generate_destin_stack(string1):
    """
    Generate the stack for a string like '{WHAT{WHO}{VERB}}'
    """
    i1 = 0
    i2 = 0
    level1 = -1
    level2 = -1
    to_found = []
    while i1 < len(string1):
        if string1[i1] == '{':
            i1 +=1
            level1+=1
            continue
        if string1[i1] == '}':
            i1 +=1
            level1-=1
            continue
        if string1[i1] == '?':
            to_found.append({'level':level1, 'match':'?'})
            i1 += 1
            continue
        if string1[i1] == '*':
            to_found.append({'level':level1, 'match':'*'})
            i1 += 1
            continue
        if re.search('[a-zA-Z:]', string1[i1]):
            temp = ''
            while re.search('[a-zA-Z:]', string1[i1]):
                temp+=string1[i1]
                i1+=1
            to_found.append({'level':level1,'match':temp})
            continue
    return to_found

def generate_dictionary( stack1, stack2, stack3 ):
    nodes_stack = []
    dictionary = {}
    for element1 in stack1:
        for element2 in stack2:
            if element1["level"] == element2["level"]:
                if element1["match"] == '?':
                    nodes_stack.append(element2["match"].split(':')[0])
                if element1["match"] == element2["match"].split(':')[1]:
                    nodes_stack.append(element2["match"].split(':')[0])
    i = 0
    for element1 in stack3:
        dictionary[element1['match']] = nodes_stack[i]
        i+=1
    return dictionary

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
    pattern = pattern.replace('?','([0-9]+:[a-zA-Z:]+)')
    pattern = pattern.replace('*','({[0-9]+:[a-zA-Z:]+({(.)*?})*})*')
    for match in matches:
        pattern = pattern.replace(match, '[0-9]+:'+match)
    return pattern

def match_patterns( regex, plain_tree ):
    match = re.search(regex, plain_tree)
    if match is None:
        return None
    return match.group()
