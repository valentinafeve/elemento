import elemento.relations as rel
import gensim.downloader as api

find_context = rel.ALL_F(
    rel.AND_F(
        rel.MATCH_TAG('NN', 'NN'),
        rel.NOT_F(rel.MATCH_REL('compound', 'compound'))
    )
)

find_pronouns = rel.ALL_F(
    rel.OR_F(
        rel.MATCH_TAG('PRP', 'PRP'),
        rel.MATCH_TAG('WP', 'WP')
    )
)


def resolve_pronouns(inspector, default_noun=None, model=None):
    context = find_context(inspector)
    pronouns = find_pronouns(inspector)
    R = {}
    for p in [prp.get('PRP') for prp in pronouns]:
        r = find_best_fit(inspector, p, context, default_noun=default_noun, model=model)
        R[p] = r
    return R


def get_neighbours(inspector, state):
    nodes = inspector.nodes
    n = state - 1 if state >= 1 else 0
    N = state + 2 if len(nodes) - state >= 2 else len(nodes)
    words = []
    for i in range(n, N):
        if i != state:
            if nodes[i]['word']:
                # TODO: Add regex
                words.append(nodes[i]['word'].lower())
    return words


def find_best_fit(inspector, pronoun_state, context, default_noun=None, model=None):
    if not model:
        model = api.load("glove-wiki-gigaword-300")
    S = 0
    R = 0
    words = get_neighbours(inspector, pronoun_state)
    nouns = [ctx.get('NN') for ctx in context]
    ss = [0]
    for word in words:
        try:
            s = model.n_similarity([pronoun_state.lower()], [word])
            ss.append(s)
        except:
            print("Word '%s' was not found in vocabulary..." % word)
        S = max(ss)
    for C in nouns:
        candidate = inspector.nodes[C]['word']
        if candidate:
            ss = [0]
            for word in words:
                try:
                    s = model.n_similarity([candidate.lower()], [word])
                    ss.append(s)
                except:
                    pass
                    print("Not found")
                    print(candidate)
                    print(word)
            s = max(ss)
            if s > S:
                S, R = s, C
    return R
