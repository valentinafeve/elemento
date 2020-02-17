import gensim.downloader as gensim
import numpy as np

#download/load model
model=gensim.load("glove-twitter-25")

v1=model["flower"]
v2=model["flowers"]
v3=model["animal"]
v4=model["cow"]
v5=model["cat"]
print(np.dot(v1,v2))
print(np.dot(v3,v4))
print(np.dot(v3,v5))
print(np.dot(v4,v5))

nubes=model["cloud"]
negro=model["black"]
tormenta=model["storm"]
effect= tormenta


cause = np.add(nubes, negro)
print(cause)
print(effect)

print(len(cause))
print(len(effect))

relation = np.cross(cause.tolist(), effect.tolist())

event = np.add(cause,  np.cross(cause, effect) )
