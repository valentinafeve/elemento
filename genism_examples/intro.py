import gensim.downloader as api

#download/load model
model=api.load("glove-twitter-25")
print("flag")
result=model.most_similar("cat")