fnsubj=MATCH_REL('WHO','nsubj')
fnmod=MATCH_REL('WHAT','dobj')
fverb=MATCH_TAG('VERB','VB')
f1=SON_F(fnsubj,1)
f2=SON_F(fnmod,1)
f3=AND_F(f1,f2)
f4=AND_F(fverb,f3)
F=SON_F(f4,-1)