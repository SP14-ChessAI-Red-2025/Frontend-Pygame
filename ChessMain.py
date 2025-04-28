import pygame
from sys import exit, argv
from pygame import Color

import chess
import renderer
import menu


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


class InputHandler():
    def __init__(self, renderer, ai_enabled, ai_player):
        self.SELECTED_PIECE = ("", 0, 0)
        self.valid_moves = []
        self.made_move = False

        self.renderer = renderer

        self.ai_enabled = ai_enabled
        self.ai_player = ai_player
        self.ai_turn = ai_enabled and (ai_player == "white" or ai_player == "both")

    def handle_click(self, engine, row, column):
        board_state = engine.board_state

        if self.SELECTED_PIECE[0] != "":
            if (self.SELECTED_PIECE[1], self.SELECTED_PIECE[2]) == (row, column):
                # Deselect the current piece if the player clicks it again
                self.SELECTED_PIECE = ("", 0, 0)
                self.valid_moves = []

            for move in self.valid_moves:
                if (7 - row, column) == target_for_move(move):
                    print(f"applying move {move}")
                    engine.apply_move(move)

                    self.SELECTED_PIECE = ("", 0, 0)
                    self.valid_moves = []

                    self.made_move = True

                    break

            if not self.made_move and self.SELECTED_PIECE != ("", 0, 0):
                self.SELECTED_PIECE = (board_state.pieces[7 - row][column].piece_type, row, column)
                self.valid_moves = moves_for_position(engine.get_valid_moves(), 7 - row, column)
        else:
            self.SELECTED_PIECE = (board_state.pieces[7 - row][column].piece_type, row, column)
            self.valid_moves = moves_for_position(engine.get_valid_moves(), 7 - row, column)

    def handle_event(self, event, engine):
        # allow to user to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Ignore the click if the AI has already made a move or if the game is over
            if self.made_move or engine.board_state.status != 0:
                return

            position = pygame.mouse.get_pos()
            column = int(position[0] / self.renderer.SQ_SIZE)
            row = int(position[1] / self.renderer.SQ_SIZE)
            
            print(f"clicked row: {row}, column: {column}")

            self.handle_click(engine, row, column)

            if self.made_move:
                self.ai_turn = self.ai_enabled

    def main_loop_iter(self, engine):
        move_targets = [target_for_move(move) for move in self.valid_moves]
                
        self.renderer.render(engine.board_state, move_targets, self.SELECTED_PIECE)

        pygame.display.update()

        self.made_move = False

        if self.ai_turn and engine.board_state.status == 0:
            self.ai_turn = self.ai_player == "both"

            print("making ai move")

            engine.ai_move(4)

            print("made ai move")

            self.made_move = True

        for event in pygame.event.get():
            self.handle_event(event, engine)
                


#initializes application window/provides game loop
def main():
    if len(argv) < 3:
        print("Must pass library path and model path on command line")
        return

    # initializes pygame
    pygame.init()


    # calculates window size and square size
    monitor_info = pygame.display.Info()
    screen_width = monitor_info.current_h * 1.25
    screen_height = monitor_info.current_h / 1.25

    # sets window size
    screen = pygame.display.set_mode((screen_width, screen_height))

    input_handler = menu.MenuInputHandler(screen)

    with chess.ChessEngine(argv[1], argv[2]) as engine:
        # render/input loop
        while True:
            # The menu input handler will return None until the user selects an option
            # After that, it will return the game settings
            ai_player = input_handler.main_loop_iter(engine)

            if ai_player is not None:
                print(f"ai_player: {ai_player}")

                # User has chosen a game mode, so replace the input handler with the main one
                input_handler = InputHandler(renderer.Renderer(screen), ai_player != "none", ai_player)


#calls main method
if __name__ == '__main__':
    main()
