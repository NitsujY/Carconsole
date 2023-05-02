import obd
from obd import OBDStatus


import random


class OBDDataSource:
    obdConnection = None
    speed = 0
    count = 0
    test_mode = False

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        if not test_mode:
            self.obdConnection = obd.Async("/dev/tty.usbserial-110")
            self.obdConnection.watch(obd.commands.SPEED, callback=self.speedCallback)
            self.obdConnection.start()

    def speedCallback(self, response):
        self.speed = int(round(response.value.magnitude))

    def getData(self):
        self.count += 1
        data = {"COUNTER": self.count}
        if not self.test_mode:
            data["OBD_STATUS"] = self.obdConnection.status()
            data["SPEED"] = self.speed
        else:
            data["OBD_STATUS"] = OBDStatus.NOT_CONNECTED
            data["SPEED"] = random.randint(0, 100)
        return data
