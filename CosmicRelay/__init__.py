from PyQtDataFramework.Core.Logging import logger
from PyQt5.QtWidgets import QApplication
import sys
from .ui import relayUIMainWindow

def main():
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')

        window = relayUIMainWindow()
        window.show()

        sys.exit(app.exec_())

    except Exception as e:
        logger.exception('Main Failed')
