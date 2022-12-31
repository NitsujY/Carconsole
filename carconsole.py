import obd
import redis
import random
from time import sleep


DRY_RUN = True
DB_KEY = "CarRuntime"


class OBD2DB():

    # Parameters
    _dryrun = False
    _runDb = True
    Interval = 0.1  # 100ms
    OBD_COMMANDS = ["SPEED", "RPM", "RUN_TIME", "FUEL_LEVEL"]

    # Runtime
    obd = None
    db = None

    def __init__(self, dryrun=False, runDb=True, interval=0.1):
        self._dryrun = dryrun
        self._runDb = runDb
        self.Interval = interval
        pass

    def __initOBD(self):
        try:
            self.obd = obd.OBD("/dev/tty.usbserial-110")
        except Exception as e:
            print(e)

    def __initDB(self):
        try:
            self.db = redis.Redis(host='localhost',
                                  port=6379,
                                  db=0)
        except Exception as e:
            print(e)

    def __obdPull(self):
        if self._dryrun:
            return {
                "SPEED": random.randint(1, 100),
                "RPM": random.randint(1, 100),
                "RUN_TIME": "Now",
                "FUEL_LEVEL": random.randint(1, 100),
            }
        else:
            data = {}
            for c in self.OBD_COMMANDS:
                if c == "SPEED":
                    data[c] = self.obd.query(
                        obd.commands.SPEED).value.magnitude
                elif c == "RPM":
                    data[c] = self.obd.query(obd.commands.RPM).value.magnitude
                elif c == "RUN_TIME":
                    data[c] = self.obd.query(
                        obd.commands.RUN_TIME).value.magnitude
                elif c == "FUEL_LEVEL":
                    data[c] = self.obd.query(
                        obd.commands.FUEL_LEVEL).value.magnitude
            return data

    def __writeDB(self, data):
        if self._dryrun:
            print(f"Writing to DB -> {data}")
        if self._runDb:
            self.db.hset(DB_KEY, mapping=data)

    def run(self):
        if not self._dryrun:
            self.__initOBD()
        if self._runDb:
            self.__initDB()
        print("Running in {} mode".format("dryrun" if self._dryrun else "OBD2"))
        while True:
            response = self.__obdPull()
            self.__writeDB(response)
            sleep(self.Interval)


def main():
    obd_to_redis = OBD2DB(dryrun=DRY_RUN)
    obd_to_redis.run()


if __name__ == '__main__':
    main()
