import pygame
from CarCom.UI.pgauge import Gauge

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY = (128, 128, 128)
COLOR_APP_BG = (60, 60, 60)
# Window size
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 600
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

    def __str__(self):
        return str(self.CarStat)

    def _drawDataSourceStatus(self, screen, status):
        Font = pygame.font.SysFont('Franklin Gothic Heavy', 50)
        statusText = Font.render(status, True, COLOR_WHITE)
        statusText_rect = statusText.get_rect(topleft=(0, 0))
        screen.blit(statusText, statusText_rect)

    def _drawSpeedGauge(self, screen):
        FONT = pygame.font.SysFont('Franklin Gothic Heavy', 50)

        gauge = Gauge(
            screen=screen,
            FONT=FONT,
            x_cord=SCREEN_CENTER_X,
            y_cord=SCREEN_CENTER_Y,
            thickness=25,
            radius=125,
            circle_colour=COLOR_GREY,
            symbol=" km/h",
            glow=True
        )
        return gauge

    def run(self):
        bg_c = COLOR_APP_BG

        # pygame
        pygame.init()
        if self.debug:
            screen = pygame.display.set_mode(
                [SCREEN_WIDTH, SCREEN_HEIGHT])
        else:
            screen = pygame.display.set_mode(
                [SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)

        running = True

        # Components init
        speedGauge = self._drawSpeedGauge(screen)

        # Main loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Datasource update
            if self.datasourceCallback:
                data = self.datasourceCallback()
                if data:
                    self.CarStat["OBD_STATUS"] = data.get("OBD_STATUS")
                    self.CarStat["RPM"] = data.get("RPM", 0)
                    self.CarStat["SPEED"] = data.get("SPEED", 0)

            # Draw
            screen.fill(bg_c)
            speedGauge.draw(percent=int(round(
                (self.CarStat["SPEED"]/CAR_MAX_SPEED)*100)),
                value=self.CarStat["SPEED"])
            self._drawDataSourceStatus(screen, self.CarStat["OBD_STATUS"])

            if self.debug:
                print(self.CarStat)

            pygame.display.flip()
            pygame.time.wait(100)

        pygame.quit()

    def setCarStat(self, info):
        pass

    def getCarStat(self):
        return self.CarStat
