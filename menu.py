import pygame

class MenuInputHandler:
    def __init__(self, screen):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.font = pygame.font.SysFont("Courier New", 128, True)

        # sets window caption and icon
        pygame.display.set_caption("ChessAI")
        window_icon = pygame.image.load("images/icon.png")
        pygame.display.set_icon(window_icon)

        '''
        self.buttons = [
            (pygame.Rect(10, 10, 400, 100), "none", "Player vs. Player"),
            (pygame.Rect(10, 210, 400, 100), "black", "Play as white vs. AI"),
            (pygame.Rect(10, 410, 400, 100), "white", "Play as black vs. AI"),
            (pygame.Rect(10, 610, 400, 100), "both", "Watch the AI play itself")
        ]
        '''
        #array of buttons images for positional calculations
        self.button_images = [
            pygame.transform.scale(pygame.image.load("images/pvp_btn.png"), (800, 100)),
            pygame.transform.scale(pygame.image.load("images/ply_wht_vs_ai.png"), (900, 100)),
            pygame.transform.scale(pygame.image.load("images/ply_blk_vs_ai.png"), (900, 100)),
            pygame.transform.scale(pygame.image.load("images/ai_vs_ai.png"), (500, 100))
        ]

        #array of rects for buttons
        self.buttons = [
            (pygame.Rect((self.screen.get_width() / 2) - (self.button_images[0].get_width() / 2), self.screenHeight / 2.5, 800, 100), "none", "Player vs. Player"),
            (pygame.Rect((self.screen.get_width() / 2) - (self.button_images[1].get_width() / 2), (self.screenHeight / 2.5) + 110, 900, 100), "black", "Play as white vs. AI"),
            (pygame.Rect((self.screen.get_width() / 2) - (self.button_images[2].get_width() / 2), (self.screenHeight / 2.5) + 220, 900, 100), "white", "Play as black vs. AI"),
            (pygame.Rect((self.screen.get_width() / 2) - (self.button_images[3].get_width() / 2), (self.screenHeight / 2.5) + 330, 500, 100), "both", "Watch the AI play itself")
        ]

        self.clicked = False

    def handle_event(self, event, engine):
        # allow to user to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()

            for rect, ai_player, _, in self.buttons:
                if rect.collidepoint(position):
                    self.clicked = True

                    self.ai_player = ai_player


    def render_menu(self):
        #draws background
        rect = pygame.Rect(0, 0, self.screenWidth, self.screenHeight)
        pygame.draw.rect(self.screen, pygame.Color("lightseagreen"), rect)

        #draws title
        img = self.font.render("Chess AI", True, pygame.Color("white"))
        self.screen.blit(img, (((self.screenWidth / 2) - (img.get_width() / 2), self.screenHeight / 10)))

        #draws menu buttons
        self.screen.blit(self.button_images[0], self.buttons[0][0])
        self.screen.blit(self.button_images[1], self.buttons[1][0])
        self.screen.blit(self.button_images[2], self.buttons[2][0])
        self.screen.blit(self.button_images[3], self.buttons[3][0])

    # This method serves two function
    # It normally performs an iteration of the main loop for the main menu, and returns None
    # When the player selects an option, it returns ai_player
    # A non-None return value tells the main loop to switch to the main InputHandler cladd
    def main_loop_iter(self, engine):
        if self.clicked:
            return self.ai_player

        self.render_menu()

        pygame.display.update()

        for event in pygame.event.get():
            self.handle_event(event, engine)
