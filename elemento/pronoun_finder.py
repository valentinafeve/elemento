import relations as rel
import tree_generator as tg
import gensim.downloader as gensim

#model=gensim.load("glove-twitter-25")
model=None

find_context=rel.ALL_F(
    rel.AND_F(
        rel.MATCH_TAG('NN','NN'),
        rel.NOT_F(rel.MATCH_REL('cmp','compound'))
    )
)

find_pronouns=rel.ALL_F(
    rel.MATCH_TAG('PRP','PRP')
)

def resolve_pronouns(inspector):
    context=find_context(inspector)
    pronouns=find_pronouns(inspector)
    R={}
    for p in [prp['PRP'] for prp in pronouns]:
        r=find_best_fit(inspector,p,context)
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

def find_best_fit(inspector,pronoun_state,context):
    S=0
    R=0
    words=get_neighbours(inspector,pronoun_state)
    for C in [ctx['NN'] for ctx in context]:
        candidate=inspector.nodes[C]['word']
        s=model.n_similarity(candidate,words)
        if s>S:
            S,R= s,C
    return R





inspector=rel.Inspector(tg.parse('the shcool bus was passed by the racecar because it was too slow').nodes)