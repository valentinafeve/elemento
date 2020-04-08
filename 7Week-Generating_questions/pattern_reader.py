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

            # Words from pattern
            wfp = re.findall(r"[\w?']+", pattern[0])
            wfp.reverse()

            # Words to match
            wtm = re.findall(r"[\w']+", pattern[1])
            wtm.reverse()
            i = 0
            F = None
            while i < len(pattern[0]):
                if pattern[0][i] == '{':
                    a = wtm.pop()
                    b = wfp.pop()
                    if b == '?':
                        b = ''
                    # Tags are uppercase
                    if b.isupper():
                        f = MATCH_TAG(a, b)
                        print("Matching tag %s %s..." % (a, b))
                    # Conll is lowercase
                    else:
                        f = MATCH_REL(a, b)
                        print("Matching rel %s %s..." % (a, b))
                    ff = SON_F(f, 1)
                    print("Creating SON relation, 1 depth")
                    if F:
                        print("Adding AND relation in F")
                        F = AND_F(F, ff)
                    else:
                        print("F created")
                        F = ff
                i+=1
            print("Adding SON relation in F, -1 depth")
            F = SON_F(F, -1)
            print("Pattern created")
            print("Adding pattern...")
            patterns.append(F)
        print("Patterns were read succesfully")
        return patterns
