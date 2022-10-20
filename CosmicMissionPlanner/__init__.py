from PyQt5.QtWidgets import QApplication
import sys
from .ui import missionPlannerMainWindow

def main():
    app = QApplication(sys.argv)
    window = missionPlannerMainWindow()
    window.show()
    sys.exit(app.exec_())
