import sys

import pygame
from network import Network

# initialize font instance
pygame.font.init()

# designated player area
width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    """
    class for creating the game buttons
    defines the x,y position on screen, color and text label

    """

    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win_):
        """
        render the button control on screen drawing a rectangle of color 1st
        then adding text on top with custom font
        :param win_: the window canvas to draw on
        :return:
        """
        pygame.draw.rect(win_, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        """
        check click event is within boundaries of button
        :param pos: x,t position of the click event
        :return: flag if the click is within button boundaries or not
        """
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win_, game_, player_):
    """
    refresh screen by drawing all assets
    :param win_: window
    :param game_: current game instance
    :param player_: current playerr
    :return:
    """
    win_.fill((128, 128, 128))  # default gery background
    if not game_.connected():  # check if the game is ready for play
        font = pygame.font.SysFont("comicsans", 80, True)
        text = font.render("Waiting for player", True, (255, 0, 0))
        win_.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:  # request player action
        font = pygame.font.SysFont("comicsans", 60, True)
        text = font.render("Your move", True, (0, 255, 0))
        win_.blit(text, (80, 100))

        text = font.render("Opponents", True, (0, 255, 0))
        win_.blit(text, (380, 100))

        # read the move made by each player
        move1 = game_.get_player_moves(0)
        move2 = game_.get_player_moves(1)

        if game_.bothWent():  # if both players made their move, display the name of the move
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
        else:
            # display status for each player based on the current move and opponents move
            if game_.p1MadeMove and player_ == 0:
                text1 = font.render(move1, True, (0, 0, 0))
            elif game_.p1MadeMove:
                text1 = font.render("Locked in", True, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", True, (0, 0, 0))

            if game_.p2MadeMove and player_ == 1:
                text2 = font.render(move2, True, (0, 0, 0))
            elif game_.p2MadeMove:
                text2 = font.render("Locked in", True, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (0, 0, 0))

        if player_ == 1:
            win_.blit(text2, (100, 350))
            win_.blit(text1, (400, 350))
        else:
            win_.blit(text1, (100, 350))
            win_.blit(text2, (400, 350))

        # draw all game buttons
        for btn in btns:
            btn.draw(win_)

    # update the display area
    pygame.display.update()


# our game play asset buttons list
btns = [Button("Rock", 50, 500, (0, 0, 0)),
        Button("Scissors", 250, 500, (255, 0, 0)),
        Button("paper", 450, 500, (0, 255, 0))
        ]


def main():
    run = True
    n = Network()  # initiate Network class instance
    clock = pygame.time.Clock()
    player = int(n.getDataObj())  # decoded text containing player id
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")  # send text "get"
        except:
            run = False
            print("couldn't get game")
            break

        if game.bothWent():  # if both players made their move
            redraw_window(win, game, player)  # update play area status
            pygame.time.delay(500)

            try:
                game = n.send("reset")  # send text "reset"
            except:
                run = False
                print("couldn't get game")
                break

            # display the final game status to both players
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!!", True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie game!!", True, (255, 0, 0))
            else:
                text = font.render("You lost ..", True, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # quit, close button clicked
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # mousedown
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    # check button click event and send each button label to server if the opposite hasn't made a
                    # move yet
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1MadeMove:
                                n.send(btn.text)
                        else:
                            if not game.p2MadeMove:
                                n.send(btn.text)

        redraw_window(win, game, player)


def menu_screen():
    """
    displays messag at start for joined player to click anywhere to start a game
    """
    run = True  # flag that game is running
    clock = pygame.time.Clock()

    # initial message asking player to click mouse button to start game
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to play!", True, (255, 255, 255))
        win.blit(text, (100, 200))
        pygame.display.update()
        for event in pygame.event.get():
            # player quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            # player pressed mouse down button
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    # when while loop is  terminated the game function main will be called
    main()


while True:
    menu_screen()
