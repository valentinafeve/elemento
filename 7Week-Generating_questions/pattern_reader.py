import re
from pattern_finder import *

class PatternReader:
    def readfromfile(self, filename):
        patterns = []
        f = open(filename, 'r+')
        lines = f.readlines()
        for line in lines:
            if line[0] == "#":
                continue

            pattern = line.split(' ')
            wfp = re.findall(r"[\w?']+", pattern[0])
            wfp.reverse()
            wtm = re.findall(r"[\w']+", pattern[1])
            wtm.reverse()

            relations = []
            parent = None

            deep = 0

            print("\n\n")
            pattern[0]+="."
            for c in pattern[0]:
                if c == '{':
                    deep+=1
                    if deep == 2:
                        if not parent:
                            print("There is a parent")
                            relations.pop()
                            parent = f

                    a = wtm.pop()
                    b = wfp.pop()

                    if b.isupper():
                        f = MATCH_TAG(a, b)
                        print("MATCH TAG %s %s..." % (a, b))
                    else:
                        f = MATCH_REL(a, b)
                        print("MATCH REL %s %s..." % (a, b))
                    if parent:
                        f = SON_F(f,1)
                        print("SON_F, deep 1")

                    relations.append(f)
                if c == '}':
                    deep-=1
                    if deep == 0:
                        f = relations.pop()
                        while relations:
                            f = AND_F(f, relations.pop())
                            print("AND_F...")
                        f = AND_F(parent, f)
                        parent = f

                    if not relations:
                        parent = SON_F(f,-1)

            patterns.append(parent)
        print("Patterns were read succesfully")
        return patterns
