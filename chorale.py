from note import Note as N
from consts import VRANGE, MAJOR_INTERVALS
import synthesizer
from scale import Scale
from harmony import Harmony

class ChordHarmonyWrapper:
    def __init__(self, chord, harmony, key):
        self.chord = chord
        self.c = self.chord
        self.harmony = harmony
        self.h = self.harmony
        self.key = key


class Chorale:
    def __init__(self, s=None, a=None, t=None, b=None, harmony=None, tonic=N("c"),intervals=MAJOR_INTERVALS):
        if s is None:
            s = []
        if a is None:
            a = []
        if t is None:
            t = []
        if b is None:
            b = []
        if harmony is None:
            harmony = []

        self.s = s
        self.a = a
        self.t = t
        self.b = b

        self.harmony = [Harmony.fromString(x) for x in harmony]

        self.scale = Scale(tonic,intervals)

        self.parts = [self.s,self.a,self.t,self.b]
    def updatechordat(self, new, position):
        for index,j in enumerate(self.parts):
            if len(j) <= position:
                j.append(new[index])
            else:
                j[position] = new[index]
    def chordat(self, position):
        chord = []
        for part in self.parts:
            if len(part) <= position:
                chord.append(None)
            else:
                chord.append(part[position])
        return ChordHarmonyWrapper(chord,self.harmony[position],self.scale)

    def getchords(self):
        return [self.chordat(x) for x in range(max([len(i) for i in self.parts]))]
    def addpart(self,part,index=-1):
        if index == -1:
            for p in range(len(self.parts)):
                if len(self.parts[p]) == 0:
                    self.parts[p].extend(part)
                    return
        else:
            self.parts[index].extend(part)

    def __repr__(self):
        return self.parts.__repr__()

    def validate(self):
        if len(self.harmony) != max([len(x) for x in self.parts]):
            raise Exception("Number of chords does not correspond to chorale length")

        for part, row in enumerate(self.parts):
            for index, note in enumerate(row):
                if note.octaveless not in self.harmony[index].cast(self.scale):
                    raise Exception("Non-chord tone in chorale (suspensions are not yet supported)")
                if not (VRANGE[part][0] <= note <= VRANGE[part][1]):
                    raise Exception("Part out of singable range")
                r = row.copy()
                r.remove(note)
    def play(self):
        player = synthesizer.Player()
        player.open_stream()
        synth = synthesizer.Synthesizer(osc1_waveform=synthesizer.Waveform.square, osc1_volume=1.0, use_osc2=False)
        for chord in self.getchords():
            print([x.__repr__()[0].upper() + x.__repr__()[1:] for x in chord.c])
            player.play_wave(synth.generate_chord([x.__repr__()[0].upper() + x.__repr__()[1:] for x in chord.c], 1.0))