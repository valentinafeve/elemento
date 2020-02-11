import nltk

file=open('ginger.txt','r')
text=file.read()
tokens = nltk.word_tokenize(text)

print("Parts: ", nltk.pos_tag(tokens))
