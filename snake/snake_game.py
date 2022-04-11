import math
import random
import sys

import pygame
import tkinter as tk
from tkinter import messagebox

width = 500  # with and height of the play window
rows = 20  # number of rows X columns of the screen grid


# used for snake body parts and the bait
class Cube(object):
    rows = 0
    w = 0

    # constructor
    # @start position of the cube :: tuple
    # @dirnx, @dirny moving direction in x and y :: int
    # @color cube :: color object
    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.color = color
        self.dirny = 0
        self.pos = start
        self.dirnx = 1

    # update the position of the cube
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # redraw the cube with each update
    # @surface draw surface
    # @eyes draw what resembles a pair of eyes
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # calculate modulo of width to number of rows
        i = self.pos[0]
        j = self.pos[1]
        border_margin_top = 1
        border_margin_bottom = 2
        # print("dis: {} i: {} j: {}".format(dis, i, j))
        # draw the a rectangular based on given coordinates
        pygame.draw.rect(surface, self.color, (i * dis + border_margin_top,
                                               j * dis + border_margin_top,
                                               dis - border_margin_bottom,
                                               dis - border_margin_bottom)
                         )
        if eyes:
            center = dis // 2  # modulo to get center of cube
            radius = 5
            circle_middle = (i * dis + center - radius, j * dis + 8)  # right circle
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)  # left circle
            #  draw circles with default color of black
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


#  the snake
class Snake(object):
    body = []  # list to hold the cube objects that make the body parts
    turns = {}  # dictionary of the number of turns the snake makes
    stopped = False

    # constructor
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)  # create a cube object a given position coordinate for the head
        self.body.append(self.head)  # add the head to the list of body parts
        self.dirnx = 0
        self.dirny = 0
        self.stopped = False

    # handles snake movement on screen through listening to key presses
    def move(self):
        if not self.stopped:
            # check events
            for event_type in pygame.event.get():
                if event_type.type == pygame.QUIT:
                    self.stopped = True
                    # pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()

                # for key in keys:
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0
                        # copy the direction  values to the head position list added to the turns list
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0
                        # copy the direction  values to the head position list added to the turns list
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        # copy the direction  values to the head position list added to the turns list
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        # copy the direction  values to the head position list added to the turns list
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            for i, c in enumerate(self.body):  # grab the index (i) and the cube (c) instance in the body
                p = c.pos[:]  # each cube instance has a position
                if p in self.turns:  # check if the position is in the turns list
                    turn = self.turns[p]
                    c.move(turn[0], turn[1])  # move to the position
                    if i == len(self.body) - 1:  # if we're at the last cube
                        self.turns.pop(p)  # remove that position list from list of turns

                else:  # check collision against boundaries of the box and move snake to opposite side
                    if c.dirnx == -1 and c.pos[0] <= 0:
                        c.pos = (c.rows - 1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                        c.pos = (0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                        c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0:
                        c.pos = (c.pos[0], c.rows - 1)
                    else:  # keep moving
                        c.move(c.dirnx, c.dirny)

    # reset everything for snake
    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # draws the cubes that make up the snake's body and head from the body list
    def draw(self, surface):
        for i, c in enumerate(self.body):
            # print("@index: {} , object: {}".format(i, c))
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    # update the snake body adding more cubes
    def add_cube(self):
        tail = self.body[-1]
        print("tail part pos x: {}, tail part pos y: {}".format(tail.dirnx, tail.dirny))
        dx, dy = tail.dirnx, tail.dirny

        #  check travel direction and add cube object to the end of snake
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        # update the last element in the body list direction x,y to dx, dy
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


def draw_grid(_w, _rows, surface):
    gap_size = _w // _rows
    x = 0
    y = 0
    for i in range(_rows):
        x = x + gap_size
        y = y + gap_size

        pygame.draw.line(surface, (255, 255, 255), (x, 0),
                         (x, _w))  # (x, 0) start position, (x, w) end position of line
        pygame.draw.line(surface, (255, 255, 255), (0, y), (_w, y))


# refresh / redraw objects on screen
def redraw_window(surface, snake, snack):
    surface.fill((0, 0, 0))
    draw_grid(width, rows, surface)
    snake.draw(surface)
    snack.draw(surface)
    pygame.display.update()


# create a random snack object on screen
def random_snack(_rows, items):
    positions = items.body

    # make sure the snack placement position doesn't overlap with moving snake body
    while True:
        x = random.randrange(_rows)
        y = random.randrange(_rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

# game end popup window
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


# game initializer
def main():
    win = pygame.display.set_mode((width, width))  # set the game board dimensions  500 x 500
    s = Snake((255, 0, 0), (10, 10))  # draw snake (head) at the center of the grid ( 20 x 20 )
    flag = True
    clock = pygame.time.Clock()
    snack = Cube(random_snack(rows, s), color=(0, 255, 0))  # draw the snack at random position on the grid
    while flag:
        pygame.time.delay(50)  # 50 millis
        clock.tick(10)  # 10 fps
        s.move()  # update snake position
        if s.body[0].pos == snack.pos:  # if snake head collides with the snack
            s.add_cube()  # add new cube to snake body
            snack = Cube(random_snack(rows, s), color=(0, 255, 0))  # create new random snack cube

        #  check if snake collides with itself
        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):
                print("Score {}".format(len(s.body)))
                message_box("You lost", "Play again..")
                s.reset((10, 10))  # reset snake position to center of game
                break

        if not s.stopped:
            redraw_window(win, s, snack)  # update the stage


Cube.rows = rows  # assign the number of rows to the rows property of the Cube object
Cube.w = width   # assign the width to the rows w of the Cube object

main()
