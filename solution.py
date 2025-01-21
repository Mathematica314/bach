import itertools
import interval
from harmony import Harmony
from consts import PREFERRED

class Solution:
    def __init__(self, notes, doubled, harmony, key):
        self.notes = notes
        self.doubled = doubled
        self.harmony = harmony
        self.key = key
        self.inversion = self.harmony.cast(self.key).index(self.notes[3].octaveless)
    def __repr__(self):
        return str(self.doubled) + " " + self.notes.__repr__() + " " + self.harmony.__repr__()
    def nextscore(self, next):
        score = 0
        # Parallels
        for pair in itertools.combinations(range(4), 2):
            self_i = self.notes[pair[0]] - self.notes[pair[1]]
            next_i = next.notes[pair[0]] - next.notes[pair[1]]
            if self_i.base == next_i.base:
                # Do not use parallel fifths or octaves
                if self_i.base == 5 or self_i.base == 1:
                    score -= 10**8
                # Use parallel thirds and sixths
                if self_i.base == 3 or self_i.base == 6:
                    score += 20
        # Voice leading
        # Leading note must rise
        if self.key.notes[6] in self.harmony.cast(self.key):
            if next.notes[[x.octaveless for x in self.notes].index(self.key.notes[6])].octaveless != self.key.notes[0]:
                score -= 10**5

        for n1,n2 in zip(self.notes,next.notes):
            score -= (n1 - n2).st()
        return score
    def calc_score(self):
        self.score = 0
        # Do not double the root in viio
        if self.harmony == Harmony.fromString("viio") and self.doubled == 0:
            self.score -= 10**5
        # In 6/4 chords the 5th must be doubled
        if self.harmony.inversion == 2 and self.doubled != 2:
            self.score -= 10**5
        # Do not double the 5th in other chords
        if self.inversion != 2 and self.doubled == 2:
            self.score -= 10**5
        # In chords iib and viio the 3rd must be doubled
        if self.harmony == Harmony.fromString("iib") or self.harmony == Harmony.fromString("viio") and self.doubled != 1:
            self.score -= 10**5
        # Never double the 3rd, apart from in chords iib,viio,iii and vi
        if self.harmony not in [Harmony.fromString("iib"),Harmony.fromString("viio"),Harmony.fromString("iii"),Harmony.fromString("vi")] and self.doubled == 1:
            self.score -= 10**5
        # Major 3rds cannot be doubled if the two notes are within 2 octaves
        if self.harmony.tonality == 1:
            for c in itertools.combinations(self.notes,2):
                if c[0].octaveless == c[1].octaveless == self.harmony.cast(self.key)[1] and c[1]-c[0] < interval.Interval(1,1,0,2):
                    self.score -= 10**5
        # Never double the 7th
        if self.doubled == 3:
            self.score -= 10**5
        # Parts should not overlap within a chord
        if sorted(self.notes,reverse=True) != self.notes:
            self.score -= 10**5
        # ii must not be in root position
        if self.harmony == Harmony.fromString("ii"):
            self.score -= 10**5

        # Prefer large gaps between the tenor and bass, and small gaps between the tenor and alto and soprano
        self.score += (self.notes[2]-self.notes[3]).st() - (self.notes[0] - self.notes[1]).st() - (self.notes[0] - self.notes[2]).st()
        # Prefer to double the root, and, if legal, the fifth and third may be doubled
        if self.doubled is not None:
            self.score += [100,0,0][self.doubled]
        # Prefer all parts to have different notes
        for pair in itertools.combinations(self.notes,2):
            if pair[0] == pair[1]:
                self.score -= 75
        # Prefer all parts to be close to the voices' respective easiest notes
        for index, note in enumerate(self.notes):
            self.score-= abs((PREFERRED[index]-note).st()) * 5

        # DO NOT YET USE 6/4 CHORDS - NOT YET IMPLEMENTED!
        if self.inversion == 2:
            self.score -= 10**10
        # CURRENTLY PREFER ROOT POSITION OVER FIRST INVERSION - TO BE CHANGED LATER
        if self.inversion == 1:
            self.score -= 40
