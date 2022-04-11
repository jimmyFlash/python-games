import os
import sys

import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800  # stage width
s_height = 700  # stage height
#  active play area
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
# grid block size
block_size = 30

# top left corner of the play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS in different rotations

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]  # list of all playable shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape

# play piece class
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x  # current x pos
        self.y = y  # current y pos
        self.shape = shape  # what shape is it
        self.color = shape_colors[shapes.index(shape)]  # what color is it
        self.rotation = 0  # current rotation


# create a 2d list 20 rows X 10 column blocks per row, each block will have default color of (0, 0, 0) -> black
# or color matching the shape in play reflecting it's position on screen
# or blocks that are filled with rows of shape parts accumulated from previous play
def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):  # loop through rows
        for j in range(len(grid[i])):  # loop through each row columns
            if (j, i) in locked_pos:  # check if the current position exists in locked_positions dictionary
                c = locked_pos[(j, i)]  # get the color corresponding to value of key (j, i) in the dictionary
                grid[i][j] = c  # update the value of color block in the game grid
    return grid


# returns list that holds play pieces positions
def convert_shape_format(piece):
    positions = []  # holds the positions of the current shape

    # get the rotated shape list
    # each shape has a number of rotated states stored in the shape's cor. list like Z or S
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):  # iterate through list of (.) and 0 representing  rotated piece

        row = list(line)  # create a new list initialized with the line of (.) and 0
        for j, column in enumerate(row):  # now iterate though that new list
            # if the value is '0'
            if column == '0':
                # append the tuple of the shape current x position on screen + j column
                #  plus shape current y on screen + i row
                positions.append((piece.x + j, piece.y + i))

    # offset the positions subtract, 2 from x to center dropped shapes w.r.t board width
    # and subtract 4 from y to offset the shape right above the play area
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


# check the grid to see if you're moving to valid space not occupied by a shape blocks
def valid_space(shape, grid):
    # created a 2D list  20 X 10 of only black colors (empty grid positions)
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # flattening the list
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:  # check if the y position of the shape is within the playable game area
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos  # deconstruct x,y values in each pos object
        if y < 1:  # reached the very top of the game box, you lose, no more moves
            return True

    return False


# returns a random shape
def get_shape():
    # create a new instance of the Piece class at x:5, y:0 and random shape
    return Piece(5, 0, random.choice(shapes))


# render any given text in the middle of the screen given the size of font, color and
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)  # set base font fo text
    label = font.render(text, True, color)  # render the Word Tetris with antialias font and white

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2,
                         top_left_y + play_height / 2 - label.get_height() / 2))


# create grid lines
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    # loop through the length of the play grid
    for i in range(len(grid)):
        # draw a horizontal lines of color grey defining grid rows
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        # loop the length of column in each grid row
        for j in range(len(grid[i])):
            # draw vertical grey lines defining grid columns
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


# remove rows of full blocks from grid
def clear_rows(grid, locked):
    inc = 0  # counter for number of rows to remove

    # loop through the length of the grid starting from bottom row moving up in negative increments of 1
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:  # check if the row contains no empty (black) spaces
            inc += 1
            ind = i  # update the index of the row
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  # remove / delete the positions matching j, i from locked postions dictionary
                except:
                    continue

    # if there are rows found to delete let shift every row down
    if inc > 0:
        # sort list of locked positions using the lambda referencing the y component
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)  # update the y value to shift the rows down
                locked[newKey] = locked.pop(key)  # update the locked list t reflect the updated / removed row

    return inc


# displays the next shape to drop
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)  # set base font fo text
    label = font.render('Next shape', True, (255, 255, 255))  # render the Word Tetris with antialias font and white

    # positioning
    sx = top_left_x + play_width + 50
    sy = top_left_y + int(play_height / 2) - 100

    # pic the shape from list of shapes and it's rotation
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    # draw the shape from data in the list of shape data
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    #  render text
    surface.blit(label, (sx + 10, sy - 30))


# draw player area and grid
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((128, 0, 0))  # use black as fill color for background
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)  # set base font fo text
    label = font.render('Py-tris', True, (255, 255, 255))  # render the Word Tetris with antialias font and white

    # current score
    font_score = pygame.font.SysFont("comicsans", 30)  # set base font fo text
    label_score = font_score.render('Score ' + str(score), True, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + int(play_height / 2) - 100

    surface.blit(label_score, (sx + 30, sy + 200))

    # highest score
    font_score = pygame.font.SysFont("comicsans", 35)  # set base font fo text
    label_score = font_score.render('Highest score: ' + str(last_score), True, (0, 255, 255))

    sx = 20
    sy = int(play_height / 2) + 100

    surface.blit(label_score, (sx, sy))

    # draw the grid rectangles updated with matching colors to simulate moving piece on the screen
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    # draw a red bounding rect
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)

    # display the text in middle of screen
    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, top_left_y - label.get_height() - 10))
    # pygame.display.update()  # refresh screen


# load the "scores.txt" that will hold highest score
# and update new high score form game
def update_score(nscore):
    # gte the path of our game directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, 'scores.txt')  # get the file for scores

    # get the max score stored
    score_ = get_max_score()

    # open the file for writing
    with open(lines, 'w') as f:
        # compare saved max score ith new score if saved score is larger
        if int(score_) > nscore:
            # write it back to the file
            f.write(str(score_))
        else:  # otherwise the new core is larger
            f.write(str(nscore))  # write it to the file for persistence


# read the max score stored int he sores.txt file
def get_max_score():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    lines = os.path.join(dir_path, 'scores.txt')
    with open(lines, 'r') as f:
        linesread = f.readlines()
        score__ = linesread[0].strip()

    return score__


#  initializer
def main(win_):
    last_score = get_max_score()  # gte last saved max score from disk
    locked_positions = {}  # holds positions that are already filled with shapes in dictionary
    grid = create_grid(locked_positions)  # create the grid with no locked positions at start

    change_piece = False  # flag to load a new piece
    run = True  # flag for running game
    current_piece = get_shape()  # load a random stat shape
    next_piece = get_shape()  # prepare the next random shape tp play
    clock = pygame.time.Clock()  # timer instance
    fall_time = 0
    fall_speed = 0.27
    level_time = 0  # represents how much time passed to make level harder
    score = 0

    while run:
        grid = create_grid(locked_positions)  # recreate the grid with updated locke positions
        fall_time += clock.get_rawtime()  # update with time in milliseconds
        level_time += clock.get_rawtime()  # update with time in milliseconds
        # print("level time {}  and fall time {}".format(level_time, fall_time))
        clock.tick()  # start clock timer

        # increase the fall speed every 5 seconds
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:  # refresh speed for updating piece position
            fall_time = 0  # reset time
            current_piece.y += 1  # update piece you property for vertical fall position
            # check if not in valid grid space and position not at start, load a new piece
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                # back position up by 1 and set change piece flag to true
                current_piece.y -= 1
                change_piece = True

        # event handlers for key presses and game exit
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # quit, close button clicked
                run = False
                sys.exit()

            # check key events
            if event.type == pygame.KEYDOWN:
                # left arrow key
                if event.key == pygame.K_LEFT:
                    # decrement current piece instance x property
                    current_piece.x -= 1
                    # check if piece is going to overlap the left boundary or occupied grid space
                    if not (valid_space(current_piece, grid)):
                        # increment piece x property to reposition
                        current_piece.x += 1
                # right arrow key
                if event.key == pygame.K_RIGHT:
                    # increment current piece instance x property
                    current_piece.x += 1
                    # check if piece is going to overlap the right boundary or occupied grid space
                    if not (valid_space(current_piece, grid)):
                        # decrement piece x property to reposition
                        current_piece.x -= 1
                #     # down arrow key
                if event.key == pygame.K_DOWN:
                    # increment current piece instance y property
                    current_piece.y += 1
                    # check if piece is going to overlap the bottom boundary or occupied grid space
                    if not (valid_space(current_piece, grid)):
                        # decrement piece y property to reposition
                        current_piece.y -= 1
                # up arrow key
                if event.key == pygame.K_UP:
                    # increment current piece instance rotation property
                    current_piece.rotation += 1
                    # check if piece is going to overlap the any boundary or occupied grid space
                    if not (valid_space(current_piece, grid)):
                        # decrement piece y property to reposition
                        current_piece.rotation -= 1

        if run:
            #  simulate the movement of the tetris piece by updating the colors of grid tiles
            shape_pos = convert_shape_format(current_piece)

            #   loop on the range of the shape_pos
            for i in range(len(shape_pos)):
                # deconstruct the tuple of x,y positions from shape list
                x, y = shape_pos[i]
                # if the y position is not < -1 , meaning the piece if visible in the grid
                if y > -1:
                    # update the color of the matching grid positions with the color value of the current piece in play
                    grid[y][x] = current_piece.color

            if change_piece:  # load anew random piece
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece  # set loaded random piece as current piece
                next_piece = get_shape()  # ready a new random shape and set to to next piece
                change_piece = False
                score += clear_rows(grid, locked_positions) * 10  # calculate score based on cleared orw count * 10

            # update play area visuals
            draw_window(win_, grid, score, last_score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

            # lost stop the game and display lost message
            if check_lost(locked_positions):
                draw_text_middle(win, "You Lost!!", 80, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(2000)  # pause fro 2 sec before going to start screen
                run = False
                update_score(score)  # updated saved highest score


def main_menu(win_):
    run = True
    while run:
        if run:
            win.fill((0, 0, 0))
            draw_text_middle(win_, "Press any key to play", 60, (255, 255, 255))
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.type != pygame.QUIT:
                main(win_)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))  # set the game screen dimensions
pygame.display.set_caption("Tetris")
main_menu(win)  # start game
