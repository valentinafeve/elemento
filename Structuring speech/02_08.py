import nltk

tokens = nltk.word_tokenize("After all, Mr. Sneelook is one of my friends. He might be even help out doing small odds and ends.")

print("Parts: ", nltk.pos_tag(tokens))
