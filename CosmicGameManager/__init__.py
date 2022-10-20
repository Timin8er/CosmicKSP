from PyQt5.QtWidgets import QApplication
import sys
from .ui import simManagerMainWindow

def main():
    app = QApplication(sys.argv)
    window = simManagerMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
