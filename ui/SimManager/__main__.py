#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
import sys
from . import simManagerMainWindow

app = QApplication(sys.argv)
window = simManagerMainWindow()
window.show()
sys.exit(app.exec_())
