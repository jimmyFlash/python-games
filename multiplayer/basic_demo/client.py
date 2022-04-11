import pygame
from network import Network
from player import Player

"""
The game client 
the actual game board with ui 

"""
width = 500
height = 500

win = pygame.display.set_mode((width, height))  # render the play area
pygame.display.set_caption("Client")


# invalidate the window and redraw assets
def redraw_window(win_, player1, player2):
    win_.fill((255, 255, 255))
    player1.draw(win_)
    player2.draw(win_)
    pygame.display.update()


def main():
    run = True
    n = Network()   # create instance of the network class
    p1 = n.getDataObj()  # request connection to server and get player status
    clock = pygame.time.Clock()

    while run:  # loop to update player client screen
        clock.tick(60)
        p2 = n.send(p1)     # send status of player current player and receive status of opposite
        for event in pygame.event.get():    # handle game exit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p1.move()  # listen to player movement with key press events
        redraw_window(win, p1, p2)


main()
