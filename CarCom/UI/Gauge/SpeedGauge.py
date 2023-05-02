import pygame


class Gauage:
    def __init__(
        self,
        screen,
        font,
        x_cord,
        y_cord,
        thickness,
        max_length,
        max_value,
        value=0,
        symbol="km/h",
        theme="DARK",
    ):
        self.screen = screen
        self.font = font
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.max_length = max_length
        self.max_value = max_value
        self.value = value
        self.symbol = symbol
        self.theme = theme

        # high performance marking
        self.bar_box_width = 5  # set the width of each box
        self.bar_box_gap = 2  # set the gap between each box
        self.high_performance_mark = int(
            self.max_length * 0.5 // (self.bar_box_width + self.bar_box_gap)
        )
        self.bar_color_low = pygame.Color("blue")
        self.bar_color_high = pygame.Color("red")

        self.bg_color_light = pygame.Color("white")
        self.box_color_light = pygame.Color("black")
        self.text_color_light = pygame.Color("black")
        self.bg_color_dark = pygame.Color("black")
        self.box_color_dark = pygame.Color("lightgray")
        self.text_color_dark = pygame.Color("white")

        if self.theme == "DARK":
            self.bg_color = self.bg_color_dark
            self.box_color = self.box_color_dark
            self.text_color = self.text_color_dark
        else:
            self.bg_color = self.bg_color_light
            self.box_color = self.box_color_light
            self.text_color = self.text_color_light

    def update(self, value):
        self.value = value

    def toggle_theme(self):
        self.theme = "LIGHT" if self.theme == "DARK" else "DARK"
        if self.theme == "DARK":
            self.bg_color = self.bg_color_dark
            self.box_color = self.box_color_dark
            self.text_color = self.text_color_dark
        else:
            self.bg_color = self.bg_color_light
            self.box_color = self.box_color_light
            self.text_color = self.text_color_light

    def draw(self):
        # draw background
        pygame.draw.rect(
            self.screen,
            self.bg_color,
            pygame.Rect(self.x_cord, self.y_cord, self.max_length, self.thickness),
        )

        # calculate length of bar and height of boxes based on current value
        length = int((self.value / self.max_value) * self.max_length)

        # draw boxes
        num_of_box = int(length // (self.bar_box_width + self.bar_box_gap))
        for i in range(num_of_box):
            box_x = self.x_cord + i * (self.bar_box_width + self.bar_box_gap)

            box_height = self.thickness

            bar_color = (
                pygame.Color("lightgrey")
                if i < self.high_performance_mark
                else pygame.Color("darkgrey")
            )
            pygame.draw.rect(
                self.screen,
                bar_color,
                pygame.Rect(box_x, self.y_cord, self.bar_box_width, box_height),
            )

        # draw text
        text_surface = self.font.render(
            f"{self.value} {self.symbol}", True, self.text_color
        )
        text_rect = text_surface.get_rect()
        text_rect.right = self.max_length + self.x_cord
        text_rect.centery = self.y_cord + (self.thickness / 2)
        self.screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    pygame.init()

    # set up display
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Speedometer Demo")

    # set up font
    font_size = 24
    font = pygame.font.SysFont(None, font_size)

    # create speedometer
    speedometer_thickness = 60
    speedometer_max_length = 500
    speedometer_x_cord = (screen_width - speedometer_max_length) // 2
    speedometer_y_cord = (screen_height - speedometer_thickness) // 2
    speedometer_bar_color = pygame.Color("grey")
    speedometer_max_value = 140
    speedometer = Gauage(
        screen,
        font,
        speedometer_x_cord,
        speedometer_y_cord,
        speedometer_thickness,
        speedometer_max_length,
        speedometer_max_value,
        theme="DARK",
    )

    # set up clock
    clock = pygame.time.Clock()

    # set initial speed
    speed = 0

    # game loop
    running = True
    while running:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                speedometer.toggle_theme()

        # update speed
        speed += 1
        if speed > speedometer_max_value:
            speed = 0

        # update speedometer
        speedometer.update(speed)

        # draw screen
        screen.fill(pygame.Color("white"))
        speedometer.draw()
        pygame.display.flip()

        # regulate framerate
        clock.tick(60)

    pygame.quit()
