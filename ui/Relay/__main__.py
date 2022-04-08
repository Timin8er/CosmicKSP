#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
import sys
from . import relayUIMainWindow

app = QApplication(sys.argv)
window = relayUIMainWindow()
window.show()
sys.exit(app.exec_())
