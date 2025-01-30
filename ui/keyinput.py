import pygame

class KeyInput:
    def __init__(self):
        self.states = [0,0,0]
        self.boxes = [[[20,100],[20,200]]]
    def run(self, screen,events):
        screen.fill("white")
        for box in self.boxes:
            pass
        pygame.draw.rect(screen,"black",pygame.rect.Rect(20,100,100,50))
