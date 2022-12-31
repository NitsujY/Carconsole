import obd
from obd import OBDStatus


class OBDDataSource():
    obdConnection = None
    speed = 0

    count = 0

    def __init__(self):
        self.obdConnection = obd.Async("/dev/tty.usbserial-110")
        self.obdConnection.watch(
            obd.commands.SPEED, callback=self.speedCallback)
        self.obdConnection.start()

    def speedCallback(self, response):
        self.speed = int(round(response.value.magnitude))

    def getData(self):
        self.count += 1
        return {
            "OBD_STATUS": self.obdConnection.status(),
            "SPEED": self.speed,
            "COUNTER": self.count,
        }
