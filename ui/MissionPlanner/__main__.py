#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
import sys
from . import missionPlannerMainWindow

app = QApplication(sys.argv)
window = missionPlannerMainWindow()
window.show()
sys.exit(app.exec_())
