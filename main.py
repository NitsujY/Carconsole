from CarCom.UI.console import CarConsoleUI
from CarCom.Interface.obd2 import OBDDataSource


def main():
    datasource = OBDDataSource(test_mode=True)

    ui = CarConsoleUI(debug=True, datasourceCallback=datasource.getData)
    # main loop
    ui.run()


if __name__ == "__main__":
    main()
