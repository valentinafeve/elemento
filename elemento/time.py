import random
import re

class Time:
    def __init__(self, string=None, keywords=None, past=False, future=False ):
        # 'ssyymmdddshhmmssms'
        self.len = 20

        self.past = False
        self.future = False

        if past:
            self.past = past

        if future:
            self.future = future

        if keywords:
            self.keywords = keywords

        if string:
            self.time = '?'*(self.len-len(string)) + string
        else:
            string = ''.join('?' for i in range(6))
            self.time = '?'*(self.len-len(string)) + string

    def __str__(self):
        return str(self.time)

    def __repr__(self):
        return str(self.time)

    def __add__(self, other):
        lleva = 0
        temp = list('?' * self.len)
        for i in range(self.len-1, 0, -1):
            a = self.time[i]
            b = other.time[i]
            if a != '?' and b != '?':
                sum = int(self.time[i]) + int(other.time[i]) + lleva
                temp[i] = str(sum)[-1]
                if sum > 9:
                    lleva = sum // 10
            else:
                if a != '?':
                    temp[i] = str(int(a) + lleva)
                    lleva = 0
                if b != '?':
                    temp[i] = str(int(b) + lleva)
                    lleva = 0
                if lleva:
                    temp[i] = str(lleva)
                    lleva = 0
        ambiguous = ''.join(i for i in temp)
        return self.__class__( ambiguous )

    def __mul__(self, other):
        lleva = 0
        temp = list('?' * self.len)
        i = self.len -1
        for a in self.time[::-1]:
            if a != '?':
                mul = int(a) * other + lleva
                temp[i] = str(mul)[-1]
                if mul > 9:
                    lleva = mul // 10
            else:
                if lleva:
                    temp[i] = str(lleva)
                    lleva = 0
            i -= 1
        ambiguous = ''.join(i for i in temp)
        return self.__class__( ambiguous )
