import elemento.relations as rel
import elemento.tree_generator as tg
import gensim.downloader as gensim
from elemento.inspector import Inspector

find_context=rel.ALL_F(
    rel.AND_F(
        rel.MATCH_TAG('NN','NN'),
        rel.NOT_F(rel.MATCH_REL('cmp','compound'))
    )
)

find_pronouns=rel.ALL_F(
    rel.MATCH_TAG('PRP','PRP')
)

def resolve_pronouns(inspector,model=None):
    context=find_context(inspector)
    pronouns=find_pronouns(inspector)
    R={}
    for p in [ prp.get('PRP') for prp in pronouns]:
        print(p)
        r=find_best_fit(inspector,p,context,model=model)
        R[p]=r
    return R

def get_neighbours(inspector,state):
    nodes=inspector.nodes
    n=state-1 if state >= 1 else 0
    N=state+2 if len(nodes)-state >= 2 else len(nodes)
    words=[]
    for i in range(n,N):
        if i!= state:
            words+=[nodes[i]['word']]
    return words

def find_best_fit(inspector,pronoun_state,context,model=None):
    if not model:
        model=gensim.load("glove-wiki-gigaword-300")
    S=0
    R=0
    words=get_neighbours(inspector,pronoun_state)
    for C in [ctx.get('NN') for ctx in context]:
        candidate=inspector.nodes[C]['word']
        if candidate:
            s=model.n_similarity(candidate,words)
            if s>S:
                S,R= s,C
    return R
