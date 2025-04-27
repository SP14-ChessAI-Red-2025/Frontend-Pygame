import pygame

class MenuInputHandler:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 48)

        self.buttons = [
            (pygame.Rect(10, 10, 400, 100), "none", "Player vs. Player"),
            (pygame.Rect(10, 210, 400, 100), "black", "Play as white vs. AI"),
            (pygame.Rect(10, 410, 400, 100), "white", "Play as black vs. AI"),
            (pygame.Rect(10, 610, 400, 100), "both", "Watch the AI play itself")
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
        for rect, _, text in self.buttons:
            pygame.draw.rect(self.screen, pygame.Color("darkblue"), rect)

            img = self.font.render(text, True, pygame.Color("antiquewhite"))
            self.screen.blit(img, (rect.left + 10, rect.top + 25))

    def main_loop_iter(self, engine):
        if self.clicked:
            return self.ai_player

        self.render_menu()

        pygame.display.update()

        for event in pygame.event.get():
            self.handle_event(event, engine)
