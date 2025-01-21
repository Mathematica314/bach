from scale import Scale
from consts import ORDER,MAJOR_INTERVALS,PHRYGIAN_INTERVALS

class Interval:
    def __init__(self,direction,base,modification,octaves=0):
        self.direction = direction
        self.base = base
        self.modification = modification
        self.octaves = octaves
    def __repr__(self):
        return ["d","m","P","M","A"][self.modification + 2]+str(self.base)+"+"*self.octaves+["v","^"][int((self.direction+1)/2)]
    def __gt__(self, other):
        return self.st() > other.st()
    def __lt__(self, other):
        return self.st() < other.st()
    def __eq__(self, other):
        return self.st() == other.st
    def __ge__(self,other):
        return self > other or self == other
    def __le__(self, other):
        return self < other or self == other

    def st(self):
        out = self.octaves*12
        if self.modification >= 0:
            return sum(MAJOR_INTERVALS[:self.base-1]) + out + [0,0,1][self.modification]
        else:
            return sum(PHRYGIAN_INTERVALS[:self.base-1]) + self.modification + 1
    @classmethod
    def fromNotes(cls,n1,n2):
        from note import Note as N
        if n1.o is None and n2.o is None:
            return min([cls.fromNotes(N(n1.p,n1.a,1),N(n2.p,n2.a,0)),
                        cls.fromNotes(N(n1.p,n1.a,1),N(n2.p,n2.a,1)),
                        cls.fromNotes(N(n1.p,n1.a,1),N(n2.p,n2.a,2))])
        direction = int(2*((n1<n2)-0.5))
        upper = max([n1,n2])
        lower = min([n1,n2])
        octaves = upper.o - lower.o
        base = list(ORDER.keys()).index(upper.p) - list(ORDER.keys()).index(lower.p) + 1
        if base < 1:
            base = base%7
            octaves -= 1
        maj_scale = Scale(lower.octaveless,MAJOR_INTERVALS)
        min_scale = Scale(lower.octaveless,PHRYGIAN_INTERVALS)
        if upper in maj_scale:
            if upper in min_scale:
                modification = 0
            else:
                modification = 1
        else:
            if upper in min_scale:
                modification = -1
            else:
                if N(upper.p,upper.a+1) in min_scale:
                    modification = -2
                else:
                    modification = 2
        return Interval(direction, base, modification,octaves)