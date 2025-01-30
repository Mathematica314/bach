from consts import NUMERALS, ORDER
from note import Note as N

class Harmony:
    def __init__(self, degree, intervals, seventh=False,inversion=0):
        self.degree = degree
        self.intervals = intervals
        self.seventh = seventh
        self.inversion = inversion
        self.tonality = {(4,3):1,(3,4):-1,(3,3):-2,(4,4):2}[self.intervals[0:2]]
    def __repr__(self):
        if self.tonality < 0:
            out = {v:k for k,v in NUMERALS.items()}[self.degree].lower()
        else:
            out = {v:k for k,v in NUMERALS.items()}[self.degree]
        if self.tonality == -2:
            out = out + "o"
        if self.tonality == 2:
            out = out + "+"
        if self.seventh:
            out = out + "7"
        return out
    def __eq__(self, other):
        return self.degree == other.degree and self.intervals == other.intervals and self.seventh == other.seventh and self.inversion == other.inversion
    def cast(self, scale):
        root = scale.notes[self.degree-1]
        out = [root]
        for i in self.intervals:
            noaccidental = N(list(ORDER.keys())[(list(ORDER.keys()).index(out[-1].p) + 2) % len(ORDER.keys())])
            out.append(N(noaccidental.p, -((noaccidental - out[-1]).st() - i)))
        return out
    @classmethod
    def fromString(cls,string):
        seventh = False
        inversion = -1
        if "a" in string:
            string = string.replace("a","")
            inversion = 0
        if "b" in string:
            string = string.replace("b","")
            inversion = 1
        if "c" in string:
            string = string.replace("c","")
            inversion = 2
        if "o" in string:
            intervals = [3,3]
            string = string.replace("o","")
        elif ord(string[0]) < 97:
            intervals = [4,3]
        else:
            intervals = [3,4]
        if "7" in string:
            seventh = True
            intervals.append(3)
            string = string.replace("7","")
        return cls(NUMERALS[string.upper()], tuple(intervals), seventh,inversion)
    @classmethod
    def fromNotes(cls, notes, scale):
        seventh = False
        intervals = [notes[i+1] - notes[i] for i in range(len(notes)-1)]
        if len(notes) == 4:
            seventh = True
        return cls(scale.notes.index(notes[0])+1,tuple(intervals), seventh)