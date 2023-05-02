import pygame
from CarCom.UI.Gauge.SpeedGauge import Gauage

DEFAULT_THEME_COLOR = "DARK"
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (128, 128, 128)
COLOR_APP_BG = (60, 60, 60)
# Window size
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 480
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
# Car specific data
CAR_MAX_SPEED = 130


class CarConsoleUI:
    CarStat = {
        "OBD_STATUS": "Not Connected",
        "SPEED": 0,
        "RPM": 0,
        "RUN_TIME": 0,
        "FUEL_LEVEL": 0,
    }

    mode = "DRY_RUN"
    debug = False

    def __init__(self, dry_run=False, debug=False, datasourceCallback=None):
        if dry_run:
            self.mode = "DRY_RUN"
        if debug:
            self.debug = debug

        if datasourceCallback:
            self.datasourceCallback = datasourceCallback

        # Theme
        self.theme = "DARK"
        self.bg_color_dark = "black"
        self.bg_color_light = "white"
        self.bg_color = self.bg_color_dark

    def __str__(self):
        return str(self.CarStat)

    def _drawDataSourceStatus(self, screen, status):
        Font = pygame.font.SysFont("Franklin Gothic Heavy", 50)
        statusText = Font.render(status, True, COLOR_WHITE)
        statusText_rect = statusText.get_rect(topleft=(0, 0))
        screen.blit(statusText, statusText_rect)

    def _drawSpeedGauge(self, screen):
        # set up font
        font_size = 48
        font = pygame.font.SysFont(None, font_size)

        speedometer_thickness = 60
        speedometer_max_length = SCREEN_WIDTH * 0.9
        speedometer_x_cord = (SCREEN_WIDTH - speedometer_max_length) // 2
        speedometer_y_cord = (SCREEN_HEIGHT - speedometer_thickness) // 2
        speedometer_bar_color = pygame.Color("blue")
        speedometer_max_value = 140
        gauge = Gauage(
            screen,
            font,
            speedometer_x_cord,
            speedometer_y_cord,
            speedometer_thickness,
            speedometer_max_length,
            speedometer_max_value,
            theme=DEFAULT_THEME_COLOR,
        )
        return gauge

    def toggle_theme(self):
        self.theme = "LIGHT" if self.theme == "DARK" else "DARK"
        if self.theme == "DARK":
            self.bg_color = self.bg_color_dark
        else:
            self.bg_color = self.bg_color_light

    def run(self):
        bg_c = COLOR_APP_BG

        # pygame
        pygame.init()
        if self.debug:
            screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        else:
            screen = pygame.display.set_mode(
                [SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN
            )

        running = True

        # Components init
        speedGauge = self._drawSpeedGauge(screen)

        # Main loop
        # Main loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.toggle_theme()
                    speedGauge.toggle_theme()

            # Datasource update
            if self.datasourceCallback:
                data = self.datasourceCallback()
                if data:
                    self.CarStat["OBD_STATUS"] = data.get("OBD_STATUS")
                    self.CarStat["RPM"] = data.get("RPM", 0)
                    self.CarStat["SPEED"] = data.get("SPEED", 0)

            # Draw
            screen.fill(self.bg_color)

            # Draw Speed gauge
            speedGauge.update(self.CarStat["SPEED"])
            speedGauge.draw()
            self._drawDataSourceStatus(screen, self.CarStat["OBD_STATUS"])

            if self.debug:
                print(self.CarStat)

            pygame.display.flip()
            pygame.time.wait(300)
        # End of Main loop

        pygame.quit()

    def setCarStat(self, info):
        pass

    def getCarStat(self):
        return self.CarStat
