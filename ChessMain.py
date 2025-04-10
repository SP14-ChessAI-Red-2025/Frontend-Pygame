import pygame
from sys import exit, argv
from pygame import Color

import chess

# defines screen size, board size, square size, and piece icon array
BOARD_SIZE = 8
SQ_SIZE = 0
SELECTED_PIECE = ("", 0, 0)
icons = []


#loads images
def load_images():
    pcs = ["wht_pawn", "wht_knight", "wht_bishop", "wht_rook", "wht_queen", "wht_king",
           "blk_pawn", "blk_knight", "blk_bishop", "blk_rook", "blk_queen", "blk_king"]
    for pc in pcs:
        icons.append(pygame.transform.scale(pygame.image.load("images/" + pc + ".png"), (SQ_SIZE, SQ_SIZE)))

#draws game board pattern
def draw_board(screen):
    colors = [pygame.Color("antiquewhite"), pygame.Color("lightseagreen")]
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            color = colors[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def icon_for_piece(piece_type, piece_player):
    assert piece_type != 0

    if piece_player == 0:
        return icons[piece_type - 1]
    else:
        return icons[6 + piece_type - 1]

#draws pieces over game board
def draw_pcs(screen, game_board, valid_moves):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            pc = game_board[7 - row][column]
            #
            pcCoords = (pc, row, column)

            if (row, column) in [(7 - move.target_position.rank, move.target_position.file) for move in valid_moves]:
                pygame.draw.circle(screen, pygame.Color("black"), center = (column * SQ_SIZE + SQ_SIZE / 2, row * SQ_SIZE + SQ_SIZE / 2), radius = SQ_SIZE / 2, width = 2)

            if pc.piece_type != 0:
                icon = icon_for_piece(pc.piece_type, pc.piece_player)

                if pcCoords != SELECTED_PIECE:
                    screen.blit(icon, pygame.Rect(SQ_SIZE * column, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))
                else:
                    screen.blit(icon, pygame.Rect(pygame.mouse.get_pos()[0] - (SQ_SIZE / 2), pygame.mouse.get_pos()[1] - (SQ_SIZE / 2), SQ_SIZE, SQ_SIZE))

def moves_for_position(valid_moves, rank, file):
    return [move for move in valid_moves if move.start_position.rank == rank and move.start_position.file == file and move.type != 5 and move.type != 6]

#initializes application window/provides game loop
def main():
    if len(argv) < 2:
        print("Must pass library path on command line")
        return

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

    with chess.ChessEngine(argv[1]) as engine:
        board_state = engine.board_state

        valid_moves = []

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

                    print(f"clicked row: {row}, column: {column}")

                    made_move = False
 
                    if SELECTED_PIECE[0] != "":
                        if (SELECTED_PIECE[1], SELECTED_PIECE[2]) == (row, column):
                            # Deselect the current piece if the player clicks it again
                            SELECTED_PIECE = ("", 0, 0)
                            valid_moves = []

                        for move in valid_moves:
                            if (row, column) == (7 - move.target_position.rank, move.target_position.file):
                                print(f"applying move {move}")
                                engine.apply_move(move)

                                SELECTED_PIECE = ("", 0, 0)
                                valid_moves = []

                                made_move = True

                                break

                        if not made_move and SELECTED_PIECE != ("", 0, 0):
                            SELECTED_PIECE = (board_state.pieces[7 - row][column], row, column)
                            valid_moves = moves_for_position(engine.get_valid_moves(), 7 - row, column)
                    else:
                        SELECTED_PIECE = (board_state.pieces[7 - row][column], row, column)
                        valid_moves = moves_for_position(engine.get_valid_moves(), 7 - row, column)                    

            #draw board & pieces
            draw_board(screen)
            draw_pcs(screen, board_state.pieces, valid_moves)

            pygame.display.update()

#calls main method
if __name__ == '__main__':
    main()
