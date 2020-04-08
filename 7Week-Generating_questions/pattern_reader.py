import re
from pattern_finder import *

class PatternReader:
    def readfromfile(self, filename):
        f = open(filename, 'r+')
        lines = f.readlines()
        for line in lines:
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
                    f = MATCH_REL(a, b)
                    print("Matching rel %s %s", (a, b))
                    ff = SON_F(f, 1)
                    if F:
                        F = AND_F(F, ff)
                    else:
                        F = ff
                i+=1
            return F
