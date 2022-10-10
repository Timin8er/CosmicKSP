from CosmicKSP.core import logger
from PyQt5.QtWidgets import QApplication
import sys
from .ui import relayUIMainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = relayUIMainWindow()
    window.show()

    sys.exit(app.exec_())
