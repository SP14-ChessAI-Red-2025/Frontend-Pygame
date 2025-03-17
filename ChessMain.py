import pygame
from sys import exit
from pygame import Color
import BoardState

# defines screen size, board size, square size, and piece icon array
BOARD_SIZE = 8
SQ_SIZE = 0
SELECTED_PIECE = ("", 0, 0)
icons = {}

#creates game board
game_board = BoardState.BoardState().game_board

#loads images
def load_images():
    pcs = ["blk_rook", "blk_knight", "blk_bishop", "blk_queen", "blk_king", "blk_pawn",
           "wht_rook", "wht_knight", "wht_bishop", "wht_queen", "wht_king", "wht_pawn"]
    for pc in pcs:
        icons[pc] = pygame.transform.scale(pygame.image.load("images/" + pc + ".png"), (SQ_SIZE, SQ_SIZE))

#draws game board pattern
def draw_board(screen):
    colors = [pygame.Color("antiquewhite"), pygame.Color("lightseagreen")]
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            color = colors[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#draws pieces over game board
def draw_pcs(screen, game_board):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            pc = game_board[row][column]
            #
            pcCoords = (pc, row, column)

            #
            if(pc != "" and pcCoords != SELECTED_PIECE):
                screen.blit(icons[pc], pygame.Rect(SQ_SIZE * column, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))
            elif(pcCoords == SELECTED_PIECE):
                screen.blit(icons[pc], pygame.Rect(pygame.mouse.get_pos()[0] - (SQ_SIZE / 2), pygame.mouse.get_pos()[1] - (SQ_SIZE / 2), SQ_SIZE, SQ_SIZE))

#initializes application window/provides game loop
def main(game_board):
    # initializes pygame
    pygame.init()

    #calculates window size and square size
    monitorInfo = pygame.display.Info()
    screenWidth = screenHeight = monitorInfo.current_h / 1.25
    global SQ_SIZE
    SQ_SIZE = screenWidth / BOARD_SIZE

    #sets window size
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    # sets window caption and icon
    pygame.display.set_caption("ChessAI")
    window_icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(window_icon)

    #loads images
    load_images()

    #create BoardState object
    #board_state = BoardState.BoardState()

    #render/input loop
    while True:
        for event in pygame.event.get():
            # allow to user to quit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                column = (int)(position[0] / SQ_SIZE)
                row = (int)(position [1] / SQ_SIZE)
                global SELECTED_PIECE
                SELECTED_PIECE = (game_board[row][column], row, column)

        #draw board & pieces
        draw_board(screen)
        draw_pcs(screen, game_board)

        pygame.display.update()

#calls main method
if __name__ == '__main__':
    main(game_board)