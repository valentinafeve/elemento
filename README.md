# Elemento

## Stanford CoreNLP installation

### Requirements
- graphviz

```bash
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
unzip stanford-corenlp-full-2018-10-05.zip
cd stanford-corenlp-full-2018-10-05
nano run.sh
```

Create an executable file _run.sh_ within
```
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
-status_port 9000 -port 9000 -timeout 15000 &
```

Some examples require [summarize!](https://github.com/despawnerer/summarize)

### Examples execution examples

#### Example 1: Getting Idea's dictionary from text

> Where "thepiratemodi" is the name of the text which must be available in books folder.

```bash
python example1.py "thepiratemodi"
```

#### Example 2: Generating questions from text

> Where "thepiratemodi" is the name of the text which must be available in books folder.

```bash
python example2.py "thepiratemodi"
```

#### Example 3: Getting Idea's dictionary from summarized text

> Where "thepiratemodi" is the name of the text which must be available in books folder and 0.4 the ratio of summarization.

```bash
python example3.py "thepiratemodi" 0.4
```

#### Example 4:  Generating questions from summarized text

> Where "thepiratemodi" is the name of the text which must be available in books folder and 0.4 the ratio of summarization.

```bash
python example3.py "thepiratemodi" 0.4
```
