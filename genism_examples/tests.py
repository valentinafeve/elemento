import gensim.downloader as api
import numpy as np

wv = api.load('word2vec-google-news-300')

cloud = wv["cloud"]
storm = wv["storm"]
chaos = wv["chaos"]

print(wv.similar_by_vector(np.subtract( storm, cloud )))
"""
>>> [('storm', 0.5948731899261475), ('hurricane', 0.4729996621608734), ('Hurricane_Dennis', 0.4634776711463928), ('Hurricane_Ivan', 0.44223684072494507), ('storms', 0.4378969073295593), ('Hurricane_Charley', 0.4260820746421814), ('flooding', 0.42498230934143066), ('Hurricane_Jeanne', 0.4158971309661865), ('Hurricane_Wilma', 0.41503629088401794), ('Wilma', 0.4097942113876343)]
"""

print(wv.similar_by_vector(np.subtract( storm, chaos )))
