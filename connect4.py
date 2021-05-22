import numpy as np
import pygame as pygame
import sys

turn = 0
pygame.init()
game_over = False
SQUARESIZE = 100
width = 7 * SQUARESIZE
height = 7 * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

def create_board():
    board = np.zeros((6,7))
    return board

    # Board index: top left corner is 0,0. bottom left is 5,0. top right is 0, 6. bottom right is 5,6 
    # board[x,y] where x refers to row (vertical), y refers to column(horizontal)


board = create_board()

def set_game_over():
    global game_over    # Needed to modify global copy of globvar
    game_over = True

def find_winner(board, piece):

    # Horizontal check
    for y in range(0,4):
        for x in range(0,6):
            if board[x, y] == piece and board[x, y+1] == piece and board[x, y+2] == piece and board[x, y+3] == piece:
                set_game_over()
                label = myfont.render("Player " + str(piece) + " wins!", 1, (0,255,0))
                screen.blit(label, (40, 10))
                return True
    
    # Vertical check. x in range(0,3) as there are 6 rows. range function is not inclusive on stop value. iterates through 0, 1, 2 (highest row index is then 5)
    for y in range(0,7):
        for x in range(0,3):
            if board[x, y] == piece and board[x+1, y] == piece and board[x+2, y] == piece and board[x+3, y] == piece:
                set_game_over()
                label = myfont.render("Player " + str(piece) + " wins!", 1, (0,255,0))
                screen.blit(label, (40, 10))
                return True

    # Diagonal checks: We need 2 diagonal checks (slanting positive and slanting negative). We then use a restricted domain and range for the start point of the diagonal
    # This restricted domain/range gives us all possible valid diagonals in the array.

    # Positive diagonal (we decrement x as the row index value is inverted (0 is top left corner)  )
    for y in range(0,4):
        for x in range(3,6):
            if board[x, y] == piece and board[x-1, y+1] == piece and board[x-2, y+2] == piece and board[x-3, y+3] == piece:
                set_game_over()
                label = myfont.render("Player " + str(piece) + " wins!", 1, (0,255,0))
                screen.blit(label, (40, 10))
                return True

    # Negative diagonal
    for y in range(0, 4):
        for x in range(0, 3):
            if board[x, y] == piece and board[x+1, y+1] == piece and board[x+2, y+2] == piece and board[x+3, y+3] == piece:
                set_game_over()
                label = myfont.render("Player " + str(piece) + " wins!", 1, (0,255,0))
                screen.blit(label, (40, 10))
                return True

    return False

def drop_piece(column, turn):

    # Search each board index with the given column value. ie column = 1, search (1,0), (1,1), (2,1) until we find a 1.
    # When we find a 1 at (column, y), set (column, y+1) = 1. (Given y+1 <= height)
    piece = 0

    if turn % 2 == 0:
        piece = 1
    else :
        piece = 2

    if board[0, column] == 1 or board[0, column] == 2:
        return False

    if board[5, column] == 0:
        board[5, column] = piece
        return True

    for y in range(0, 6):
        if board[y, column] == 1 or board[y, column] == 2:
            board[y - 1, column] = piece
            return True


def draw_board(board):
    for y in range(6):
        for x in range(7):
            pygame.draw.rect(screen, (0,0,255), (x * SQUARESIZE, y * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE) )
            if board[y, x] == 0:
                pygame.draw.circle(screen, (0,0,0), (int(x * SQUARESIZE + SQUARESIZE/2), int((y+1)* SQUARESIZE + SQUARESIZE/2)), int(SQUARESIZE/2 - 5))
            elif board[y, x] == 1:
                pygame.draw.circle(screen, (255,0,0), (int(x * SQUARESIZE + SQUARESIZE/2), int((y+1)* SQUARESIZE + SQUARESIZE/2)), int(SQUARESIZE/2 - 5))
            else:
                pygame.draw.circle(screen, (255,255,0), (int(x * SQUARESIZE + SQUARESIZE/2), int((y+1)* SQUARESIZE + SQUARESIZE/2)), int(SQUARESIZE/2 - 5))
    pygame.display.update()


draw_board(board)
while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        # Print circles at top of screen
        if (event.type == pygame.MOUSEMOTION):
            pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn % 2 == 0:
                pygame.draw.circle(screen, (255,0,0), (posx, int(SQUARESIZE/2)), SQUARESIZE/2 - 5)
            else:
                pygame.draw.circle(screen, (255,255,0), (posx, int(SQUARESIZE/2)), SQUARESIZE/2 - 5)
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, (0,0,0), (0,0, width, SQUARESIZE))
            
            # Ask player 1 input
            if turn % 2 == 0:
                selection = int(event.pos[0] / 100)
                if not drop_piece(selection, turn):
                    continue
                find_winner(board, 1)   
            # Ask player 2 input
            else:
                selection = int(event.pos[0] / 100)
                if not drop_piece(selection, turn):
                    continue
                find_winner(board, 2)

            # Increment turn count, check for winners.
            draw_board(board)  
            turn += 1

    if game_over:
        pygame.time.wait(3000)