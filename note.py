class Note:
    def __init__(self,pitch,accidental=0,octave=None):
        self.p = pitch
        self.a = accidental
        self.o = octave
        if self.o is None:
            self.octaveless = self
        else:
            self.octaveless = Note(self.p,self.a)
    def getWithinOctave(self):
        from consts import ORDER
        return ORDER[self.p] + self.a
    def smtsub(self, other):
        if self.o is None:
            if self.getWithinOctave() > other.getWithinOctave():
                return (self.getWithinOctave() - other.getWithinOctave())%12
            else:
                return (self.getWithinOctave() - other.getWithinOctave() + 12)%12
        else:
            return (self.o - other.o)*12 + self.getWithinOctave() - other.getWithinOctave()
    def __repr__(self):
        if self.a==0:
            if self.o==None:
                return self.p
            return self.p+str(self.o)
        if self.o==None:
            return self.p + ["bb","b",None,"#","##"][self.a+2]
        return self.p + ["bb","b",None,"#","##"][self.a+2]+str(self.o)
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        if self.o is None:
            return self.p == other.p and self.a == other.a
        return self.o*12 + self.getWithinOctave() + self.a == other.o*12 + other.getWithinOctave() + other.a
    def __lt__(self,other):
        if type(other) != type(self):
            raise TypeError(f"\'<\' not supported between instances of \'{type(self)}\' and \'{type(other)}\'")
        if self.o is None or other.o is None:
            raise Exception("Cannot compare non-octave-marked notes")
        if self.o < other.o:
            return True
        if other.o < self.o:
            return False
        return self.getWithinOctave() < other.getWithinOctave()
    def __gt__(self,other):
        if type(other) != type(self):
            raise TypeError(f"\'<\' not supported between instances of \'{type(self)}\' and \'{type(other)}\'")
        if self.o is None or other.o is None:
            raise Exception("Cannot compare non-octave-marked notes")
        if self.o > other.o:
            return True
        if other.o > self.o:
            return False
        return self.getWithinOctave() > other.getWithinOctave()
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    def __sub__(self, other):
        import interval
        return interval.Interval.fromNotes(self,other)
    def __add__(self, other):
        return (self.o + other.o)*12 + self.getWithinOctave() + other.getWithinOctave()
    @classmethod
    def fromstring(cls,string):
        if string[1] in "#b":
            return cls(string[0], ["bb","b",None,"#","##"].index(string[1:-1])-2, int(string[-1]))
        return cls(string[0], 0, int(string[1]))

    def lily(self):
        if self.o == 3:
            return self.p
        elif self.o < 3:
            str = self.p
            for j in range(3-self.o):
                str = str+","
        else:
            str = self.p
            for j in range(self.o-3):
                str = str + "\'"
        return str