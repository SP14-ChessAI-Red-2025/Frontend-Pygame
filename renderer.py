import pygame
from pygame import Color

class Renderer:
    def __init__(self, screen):
        # defines screen size, board size, square size, and piece icon array
        self.BOARD_SIZE = 8
        self.icons = []
        self.SQ_SIZE = screen.get_height() / self.BOARD_SIZE
        self.screen = screen

        self.sidebar_width = screen.get_width() - screen.get_height()

        # sets window caption and icon
        pygame.display.set_caption("ChessAI")
        window_icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(window_icon)

        #loads images
        self.load_images()

        #loads side bar image
        self.sideBarImage = pygame.transform.scale(pygame.image.load("images/side_bar.png"), (self.sidebar_width, screen.get_height()))

        #loads button images
        self.drawButton = pygame.transform.scale(pygame.image.load("images/draw_btn.png"), (300, 100))
        self.resignButton = pygame.transform.scale(pygame.image.load("images/resign_btn.png"), (375, 100))

        #creates rect for buttons
        self.drawBtnRect = pygame.Rect(((self.screen.get_width()) - (self.sidebar_width / 2)) - (self.drawButton.get_width() / 2), (self.screen.get_height() / 3), 300, 100)
        self.resignBtnRect = pygame.Rect(((self.screen.get_width()) - (self.sidebar_width / 2)) - (self.resignButton.get_width() / 2), (self.screen.get_height() / 2), 375, 100)

        self.font = pygame.font.SysFont("Courier New", 36, True)

    #loads images
    def load_images(self):
        pcs = ["wht_pawn", "wht_knight", "wht_bishop", "wht_rook", "wht_queen", "wht_king",
            "blk_pawn", "blk_knight", "blk_bishop", "blk_rook", "blk_queen", "blk_king"]
        for pc in pcs:
            self.icons.append(pygame.transform.scale(pygame.image.load("images/" + pc + ".png"), (self.SQ_SIZE, self.SQ_SIZE)))

    #draws game board pattern
    def draw_board(self):
        colors = [pygame.Color("antiquewhite"), pygame.Color("lightseagreen")]
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                color = colors[(row + column) % 2]
                pygame.draw.rect(self.screen, color, pygame.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def icon_for_piece(self, piece_type, piece_player):
        assert piece_type != 0

        if piece_player == 0:
            return self.icons[piece_type - 1]
        else:
            return self.icons[6 + piece_type - 1]

    #draws pieces over game board
    def draw_pcs(self, game_board, move_targets, SELECTED_PIECE):
        SQ_SIZE = self.SQ_SIZE
        
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                pc = game_board[7 - row][column]
                
                pcCoords = (pc.piece_type, row, column)

                if (7 - row, column) in move_targets:
                    pygame.draw.circle(self.screen, pygame.Color("black"), center = (column * SQ_SIZE + SQ_SIZE / 2, row * SQ_SIZE + SQ_SIZE / 2), radius = SQ_SIZE / 2, width = 2)

                if pc.piece_type != 0:
                    icon = self.icon_for_piece(pc.piece_type, pc.piece_player)

                    if pcCoords != SELECTED_PIECE:
                        self.screen.blit(icon, pygame.Rect(SQ_SIZE * column, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))
                    else:
                        self.screen.blit(icon, pygame.Rect(pygame.mouse.get_pos()[0] - (SQ_SIZE / 2), pygame.mouse.get_pos()[1] - (SQ_SIZE / 2), SQ_SIZE, SQ_SIZE))

    def draw_status(self, board_state):
        status_str = ["Normal", "Draw", "Checkmate", "Resigned"][board_state.status]
        img = self.font.render(f"STATUS: {status_str}", True, pygame.Color("antiquewhite"))
        #self.screen.blit(img, (self.screen.get_height() + 10, 20))
        self.screen.blit(img, (((self.screen.get_width() - self.sidebar_width) + (self.sidebar_width / 2)) - (img.get_width() / 2), 20))

    def render(self, board_state, move_targets, SELECTED_PIECE):
        #draw board & pieces
        self.draw_board()
        self.draw_pcs(board_state.pieces, move_targets, SELECTED_PIECE)

        #draw sidebar
        rect = pygame.Rect(self.screen.get_height(), 0, self.sidebar_width, self.screen.get_height())
        self.screen.blit(self.sideBarImage, rect)
        #pygame.draw.rect(self.screen, pygame.Color("darkslategray"), rect)

        #draw buttons
        self.screen.blit(self.drawButton, self.drawBtnRect)
        self.screen.blit(self.resignButton, self.resignBtnRect)

        self.draw_status(board_state)
        
