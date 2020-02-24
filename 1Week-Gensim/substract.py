import gensim.downloader as api
import numpy as np

wv = api.load('word2vec-google-news-300')

cloud = wv["cloud"]
storm = wv["storm"]
chaos = wv["chaos"]

print(wv.similar_by_vector(np.subtract( storm, cloud )))
print(wv.similar_by_vector(np.subtract( storm, chaos )))
