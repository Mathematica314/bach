from note import Note as N
from consts import ORDER

class Scale:
    def __init__(self, tonic, intervals):
        self.intervals = intervals
        self.tonic = tonic
        self.notes = [tonic]
        for i in range(len(self.intervals)):
            noaccidental = N(list(ORDER.keys())[(list(ORDER.keys()).index(self.notes[i].p) + 1)%len(ORDER.keys())])
            self.notes.append(N(noaccidental.p, -((noaccidental.getWithinOctave()-self.notes[i].getWithinOctave())%12 - self.intervals[i])))
    def __repr__(self):
        return str(self.notes)
    def __contains__(self, other):
        if other.octaveless in self.notes:
            return True
        return False
    def __index__(self, other):
        return self.notes.index(other.octaveless)