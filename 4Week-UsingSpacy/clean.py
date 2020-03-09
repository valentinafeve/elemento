import re

FILE_REPLC=""
REP={}

def replace(file_replc,s):
    global FILE_REPLC
    global REP
    if file_replc!=FILE_REPLC:
        FILE_REPLC=file_replc
        REP={}
        f = open(file_replc, "r")
        for L in f.readlines():
            rule=L.split(' ')
            REP[rule[0]]=rule[1][:-1]
    '''
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
    pattern = re.compile("|".join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], s)
    '''
    for k in REP:
        s=s.replace(k,REP[k])

    return s