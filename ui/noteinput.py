import pygame

class NoteInput:
    def __init__(self):
        self.notes = []
        self.tclef = pygame.image.load("ui/img.png")
        self.tclef = pygame.transform.scale(self.tclef,(59*2,200))

    def run(self,screen,events):
        y = pygame.mouse.get_pos()[1]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.notes.append(y-y%12+8)
        screen.fill("white")
        for i,note in enumerate(self.notes[:-11:-1]):
            if note < 140:
                for j in range(note+12, 152, 24):
                    adj = 0
                    if note%24 == 8:
                        adj = -12
                    pygame.draw.line(screen, "black", (585-50*i, j+adj), (615-50*i, j+adj), 3)
            if note > 260:
                for j in range(260,note-11, 24):
                    pygame.draw.line(screen, "black", (585-50*i, j+12), (615-50*i, j+12), 3)
                print(note)
            pygame.draw.circle(screen, "black", (600-50*i,note), 10)
        pygame.draw.circle(screen, (92, 92, 92), (650,y-y%12+8), 10)
        for i in range(8,152,24):
            pygame.draw.line(screen,"black",(635,i),(665,i),3)
        pygame.draw.line(screen, "black", (0, 152), (800, 152), 3)
        pygame.draw.line(screen, "black", (0, 176), (800, 176), 3)
        pygame.draw.line(screen, "black", (0, 200), (800, 200), 3)
        pygame.draw.line(screen, "black", (0, 224), (800, 224), 3)
        pygame.draw.line(screen, "black", (0, 248), (800, 248), 3)
        for i in range(248+24,400,24):
            pygame.draw.line(screen,"black",(635,i),(665,i),3)
        screen.blit(self.tclef,(-25,105))
