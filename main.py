from CarCom.UI.console import CarConsoleUI
from CarCom.Interface.obd2 import OBDDataSource


def main():
    datasource = OBDDataSource()

    ui = CarConsoleUI(debug=True, datasourceCallback=datasource.getData)
    ui.run()


if __name__ == '__main__':
    main()
