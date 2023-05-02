class ThemeButton:
    COLOR_LIGHT_BG = (255, 255, 255)
    COLOR_LIGHT_TEXT = (0, 0, 0)
    COLOR_DARK_BG = (60, 60, 60)
    COLOR_DARK_TEXT = (255, 255, 255)

    def __init__(self, screen):
        self.screen = screen
        self.width = 50
        self.height = 30
        self.bg_color = COLOR_GREY
        self.text_color = COLOR_WHITE
        self.font = pygame.font.SysFont(None, 20)
        self.dark_mode = False
        self.rect = pygame.Rect(
            SCREEN_WIDTH - self.width - 10, 10, self.width, self.height
        )
        self.update()

    def update(self):
        if self.dark_mode:
            self.bg_color = COLOR_LIGHT_BG
            self.text_color = COLOR_LIGHT_TEXT
            text = self.font.render("Light", True, self.text_color)
        else:
            self.bg_color = COLOR_DARK_BG
            self.text_color = COLOR_DARK_TEXT
            text = self.font.render("Dark", True, self.text_color)
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(
            text,
            (
                self.rect.centerx - text.get_width() / 2,
                self.rect.centery - text.get_height() / 2,
            ),
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dark_mode = not self.dark_mode
                self.update()
