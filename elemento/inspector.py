class Inspector():
    def __init__(self,nds,st=0):
        self.nodes=nds
        self.state=st

    def children(self):
        R=[]
        deps=self.nodes[self.state]['deps']
        for r in deps:
            R+=[Inspector(self.nodes,deps[r][0])]
        return R

    def get_tag(self):
        return self.nodes[self.state]['tag']

    def get_rel(self):
        if self.state==0:
            return 'None'
        return self.nodes[self.state]['rel']

    def get_lemma(self):
        return self.nodes[self.state]['lemma']

    def get_state(self):
        return self.state
