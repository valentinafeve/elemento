import os
from nltk.parse import stanford
os.environ['STANFORD_PARSER'] = '/home/gustavo/Downloads/stanford-parser-full-2018-10-17'
os.environ['STANFORD_MODELS'] = '/home/gustavo/Downloads/stanford-parser-full-2018-10-17'

parser = stanford.StanfordParser(model_path="/location/of/the/englishPCFG.ser.gz")
sentences = parser.raw_parse_sents(("Hello, My name is Melroy.", "What is your name?"))
print(sentences)

# GUI
for line in sentences:
    for sentence in line:
        sentence.draw()