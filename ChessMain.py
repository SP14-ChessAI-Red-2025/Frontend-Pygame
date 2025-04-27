import pygame
from sys import exit, argv
from pygame import Color

import chess
import render


SELECTED_PIECE = ("", 0, 0)


# Given a chess move, return the square that must be clicked to apply the move
# For most moves, this is just move.target_position, but castling needs special handling
def target_for_move(move):
    if move.type in [5, 6]:
        raise Exception("Claiming a draw and resignation don't have target positions")
    if move.type == 3:
        if move.start_position.file == 0:
            return (move.start_position.rank, 2)
        else:
            return (move.start_position.rank, 6)

    return (move.target_position.rank, move.target_position.file)

def moves_for_position(valid_moves, rank, file):
    # Don't include moves of type castle, claim_draw, or resign, as they interpret move.target_position differently
    moves = [move for move in valid_moves if move.start_position.rank == rank and move.start_position.file == file and move.type not in [3, 5, 6]]
    
    # If the user clicks on the king, add any castling moves to the list
    # This is mixing the UI with game logic a bit too much for my taste, but it works
    if (rank == 0 or rank == 7) and file == 4:
        castle_moves = [move for move in valid_moves if move.type == 3 and move.start_position.rank == rank]

        moves += castle_moves
        

    return moves

#initializes application window/provides game loop
def main():
    if len(argv) < 3:
        print("Must pass library path and model path on command line")
        return

    ai_enabled = False

    if len(argv) > 3 and argv[3] in ["True", "true"]:
        ai_enabled = True

    ai_player = "black"

    if len(argv) > 4 and argv[4] in ["white", "White", "black", "Black"]:
        ai_player = argv[4].lower()

    # initializes pygame
    pygame.init()

    renderer = render.Renderer()

    ai_turn = ai_enabled and ai_player == "white"

    with chess.ChessEngine(argv[1], argv[2]) as engine:
        board_state = engine.board_state

        valid_moves = []

        #render/input loop
        while True:
            if ai_turn:
                ai_turn = False

                print("making ai move")
                engine.ai_move(4)

                continue

            for event in pygame.event.get():
                # allow to user to quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    column = (int)(position[0] / renderer.SQ_SIZE)
                    row = (int)(position [1] / renderer.SQ_SIZE)

                    global SELECTED_PIECE

                    print(f"clicked row: {row}, column: {column}")

                    made_move = False
 
                    if SELECTED_PIECE[0] != "":
                        if (SELECTED_PIECE[1], SELECTED_PIECE[2]) == (row, column):
                            # Deselect the current piece if the player clicks it again
                            SELECTED_PIECE = ("", 0, 0)
                            valid_moves = []

                        for move in valid_moves:
                            if (7 - row, column) == target_for_move(move):
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

                    if made_move:
                        ai_turn = ai_enabled

            move_targets = [target_for_move(move) for move in valid_moves]
            renderer.render(board_state, move_targets, SELECTED_PIECE)

            pygame.display.update()


#calls main method
if __name__ == '__main__':
    main()
