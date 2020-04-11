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
                if c == '}':
                    deep-=1
                    print("Found }")
                    print(deep)
                    if deep == 0:
                        f = relations.pop()
                        while relations:
                            f = AND_F(f, relations.pop())
                            print("AND...")
                        if parent:
                            f = AND_F(parent, f)
                            print("AND...")
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
                        ff = SON_F(f,1)
                        print("SON, deep 1")
                    else:
                        ff = SON_F(f,-1)
                        print("SON, deep -1")

                    relations.append(ff)
                if c == '{':
                    deep+=1
                    print("Found {")
                    print(deep)
            patterns.append(parent)
        print("Patterns were read succesfully")
        return patterns
