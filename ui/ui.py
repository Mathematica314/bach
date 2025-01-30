import pygame
import keyinput,noteinput

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

running = True

kin = keyinput.KeyInput()
nin = noteinput.NoteInput()

curr_screen = kin

while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    curr_screen.run(screen,events)
    pygame.display.flip()
pygame.quit()