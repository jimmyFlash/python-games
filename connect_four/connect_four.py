import numpy as np
import pygame
import sys
import math

# colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#  board setup
ROW_COUNT = 6
COLUMN_COUNT = 7

INVALID_COLUMNS_INDECIES = 3  # constant used for checking invalid column/row range indices

#  list of player moves
player_1_moves = []
player_2_moves = []

SQUARESIZE = 100  # size of the tile

#  initialize variables
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)  # radius of the circle for players and holes


# 2d matrix of 6 rows by 7 columns with default values of 0 for board
def create_board():
    board_ = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board_


# set position of a player piece to store itn he board array
def drop_piece(board_, row_, col_, piece):
    board_[row_][col_] = piece


# check if the position on board is valid ( not filled with either player tiles)
def is_valid_location(board_, col_):
    return board_[ROW_COUNT - 1][col_] == 0  # remember [ROW_COUNT - 1] is because we have an extra row for player move


# check if position on board is empty
def get_next_open_row(board_, col_):
    for row_ in range(ROW_COUNT):
        offset = ROW_COUNT - 1 - row_
        print(offset)
        if board_[row_][col_] == 0:
            return row_


#  flip the console board to drop pieces to the bottom not fill form top
def print_board_flipped_x(board_):
    print(np.flip(board_, 0))


# calculate of the move is a win move for the player 
def winning_move(board_, piece_):
    # loop in the array to figure out the winning connection (vertical)
    for column_ in range(COLUMN_COUNT - INVALID_COLUMNS_INDECIES):
        for row_ in range(ROW_COUNT):
            if board_[row_][column_] == piece_ and board_[row_][column_ + 1] == piece_ and board_[row_][
                column_ + 2] == piece_ and board_[row_][column_ + 3] == piece_:
                return True

    # loop in the array to figure out the winning connection (horizontal)
    for column_ in range(COLUMN_COUNT):
        for row_ in range(ROW_COUNT - INVALID_COLUMNS_INDECIES):
            if board_[row_][column_] == piece_ and board_[row_ + 1][column_] == piece_ and board_[row_ + 2][
                column_] == piece_ and board_[row_ + 3][column_] == piece_:
                return True

    # Check positively sloped diagonals  \
    for column_ in range(COLUMN_COUNT - INVALID_COLUMNS_INDECIES):
        for row_ in range(ROW_COUNT - INVALID_COLUMNS_INDECIES):
            if board_[row_][column_] == piece_ and board_[row_ + 1][column_ + 1] == piece_ and board_[row_ + 2][
                column_ + 2] == piece_ and board_[row_ + 3][column_ + 3] == piece_:
                return True

    # Check negatively sloped diagonals /
    for column_ in range(COLUMN_COUNT - INVALID_COLUMNS_INDECIES):
        for row_ in range(INVALID_COLUMNS_INDECIES, ROW_COUNT):
            if board_[row_][column_] == piece_ and board_[row_ - 1][column_ + 1] == piece_ and board_[row_ - 2][
                column_ + 2] == piece_ and board_[row_ - 3][column_ + 3] == piece_:
                return True


# create playing board ui
def draw_board(board_):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    #  create player 1 filled color tile
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board_[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)

            #  create player 2 filled color tile
            elif board_[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)
    pygame.display.update()


board = create_board()  # draw board ui
print_board_flipped_x(board)  # flip board to fill form bottom to top

game_over = False
turn = 0  # player turn

pygame.init()
myfont = pygame.font.SysFont("monospace", 75)  # using custom font

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

#  update the game as long as the game over flag is not true
while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # quit, close button clicked
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # draw a black rectangle to cover up the circle trail as mouse moved
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posX = event.pos[0]
            if turn == 0:
                # render player one red circle and move it with mouse
                pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE / 2)), RADIUS)

            else:
                # render player two red circle and move it with mouse
                pygame.draw.circle(screen, YELLOW, (posX, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:  # mousedown
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # ask for player 1 input
            if turn == 0:
                posX = event.pos[0]
                col = int(math.floor(posX / SQUARESIZE))
                pygame.draw.circle(screen, YELLOW, (posX, int(SQUARESIZE / 2)), RADIUS)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render("Player-1 wins!!!", True, RED)
                    screen.blit(label, (40, 10))
                    game_over = True



            # # ask for player 2 input
            else:
                posX = event.pos[0]
                col = int(math.floor(posX / SQUARESIZE))
                pygame.draw.circle(screen, RED, (posX, int(SQUARESIZE / 2)), RADIUS)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("Player-2 wins!!!", True, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board_flipped_x(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(2000)
