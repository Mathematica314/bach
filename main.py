from note import Note as N
import csv, itertools, networkx, subprocess, pygame, copy
from chorale import Chorale
from solution import Solution
from consts import VRANGE, MAJOR_INTERVALS

print("IMPORTS INITIALISED")

OCTAVE_TRIAL_RANGE = (2,5)

with open("chorale.bach") as file:
    reader = csv.reader(file)
    for index, row in enumerate(reader):
        if index == 0:
            tonic = N(row[0])
            tonality = MAJOR_INTERVALS
        elif index == 1:
            chorale = Chorale(harmony=[x.strip() for x in row], tonic=tonic, intervals=tonality)
        else:
            chorale.addpart([N.fromstring(x.strip()) for x in row], index-2)

chorale.validate()
solutions = []


chordnum = 0

for chord in chorale.getchords():
    row_solutions = []
    doublings = []
    for d_index, double in enumerate(chord.h.cast(chorale.scale)):
        notes = chord.h.cast(chorale.scale) + [double]
        for note in chord.c:
            if note is not None and note.octaveless in notes:
                notes.remove(note.octaveless)
                doublings.append(notes)
            elif note is not None:
                break
    for doub_in,notes in enumerate(doublings):
        for perm in itertools.permutations([i for i,j in enumerate(chord.c) if j is None]):
            # Inversion checking
            legal = True
            if 3 in perm:
                inv = chord.h.cast(chorale.scale).index(notes[-1])
                if chord.h.inversion == -1 and not (inv == 0 or inv == 1):
                    legal = False
                if chord.h.inversion != -1 and chord.h.inversion != inv:
                    legal = False
            if legal:
                ch = chord.c.copy()
                octave_solutions = []
                for i,part in enumerate(perm):
                    part_octave_solutions = []
                    ch[part] = notes[i]
                    for octave in range(*OCTAVE_TRIAL_RANGE):
                        if VRANGE[part][0] <= N(notes[i].p,notes[i].a,octave) <= VRANGE[part][1]:
                            part_octave_solutions.append((part,N(notes[i].p,notes[i].a,octave)))
                    octave_solutions.append(part_octave_solutions)
                for solution in itertools.product(*octave_solutions):
                    ch_oct = ch.copy()
                    for note in solution:
                        ch_oct[note[0]] = note[1]
                    hrm = copy.deepcopy(chord.h)
                    hrm.inversion = hrm.cast(chorale.scale).index(ch_oct[3].octaveless)
                    sol = Solution(ch_oct,doub_in,hrm,chorale.scale)
                    sol.calc_score()
                    row_solutions.append(sol)
    solutions.append(row_solutions)
    chordnum += len(row_solutions)

print(f"{chordnum} CHORDS INITIALISED")

begin = object()
end = object()
gr = networkx.Graph()

edgenum = 0

for i in solutions[0]:
    gr.add_edge(begin, i, weight=10**10-i.score)
    edgenum += 1
for i in solutions[-1]:
    gr.add_edge(i, end, weight=0)
    edgenum += 1
current_layer = solutions[0]
next_layer = 1

for next_layer in range(1,len(solutions)):
    for curr in current_layer:
        for next_chord in solutions[next_layer]:
            gr.add_edge(curr,next_chord,weight=10**10-curr.nextscore(next_chord)-next_chord.score)
            edgenum += 1
    current_layer = solutions[next_layer]
    next_layer += 1

print(f"{edgenum} EDGES CALCULATED")

path = networkx.shortest_path(gr,begin,end,weight="weight")

print("PATH CALCULATED")

out_rows = [[] for i in range(4)]
for index,node in enumerate(path[1:-1]):
    chorale.updatechordat(node.notes, index)
    row = [x.lily() for x in node.notes]
    for index,note in enumerate(row):
        out_rows[index].append(note)
out_strings = ["","","",""]
for index,row in enumerate(out_rows):
    for note in row:
        out_strings[index] = out_strings[index] + " " + note
replacements = {"[s]":out_strings[0],"[a]":out_strings[1],"[t]":out_strings[2],"[b]":out_strings[3]}

with open("template") as tmp:
    with open("out","w") as out:
        for row in tmp:
            for key in replacements.keys():
                row = row.replace(key,replacements[key])
            out.write(row)

subprocess.run(["lilypond","--png","out"])

pygame.init()
img = pygame.image.load("out.cropped.png")

screen = pygame.display.set_mode(img.get_size())

screen.blit(img, (0,0))
pygame.display.flip()

chorale.play()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()