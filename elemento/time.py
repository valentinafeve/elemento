import random
import re

class Time:
    def __init__(self, string=None, past=False, future=False ):
        # 'ssyymmdddshhmmssms'
        self.len = 20

        self.past = False
        self.future = False
        self.words = []

        if past:
            self.past = past

        if future:
            self.future = future

        if string:
            sign = False
            if string[-1] == '+':
                self.time = '?'*(self.len-len(string)+1) + string[:-1]
                self.future = True
                sign = True

            if string[-1] == '-':
                self.time = '?'*(self.len-len(string)+1) + string[:-1]
                self.past = True
                sign = True

            if not sign:
                self.time = '?'*(self.len-len(string)) + string

        else:
            nums = ['1','2','3','4','5','6','7','8','9','0','?','?']
            string = ''.join(random.choice(nums) for i in range(6))
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

    def __sub__(self, other):
        lleva = 0
        temp = list('?' * self.len)
        for i in range(self.len-1, 0, -1):
            a = self.time[i]
            b = other.time[i]
            if a != '?' and b != '?':
                sub = int(self.time[i]) - int(other.time[i]) - lleva
                if sub < 0:
                    sub = 10 + int(self.time[i]) - int(other.time[i]) - lleva
                    lleva = 1
                print(sub)
                temp[i] = str(sub)[-1]
            else:
                if a != '?':
                    temp[i] = str(int(a) - lleva)
                    lleva = 0
                if b != '?':
                    temp[i] = str(int(b))
                    lleva = 0
                if lleva:
                    temp[i] = str(0)
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

    def get_time( words, time_dictionary ):
        time = Time()
        for word in words:
            for k, time_temp in time_dictionary.items():
                if k == word:
                    time += time_temp
        return time
