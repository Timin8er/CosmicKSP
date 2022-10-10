#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
import sys
from .ui import relayUIMainWindow

app = QApplication(sys.argv)
app.setStyle('Fusion')

window = relayUIMainWindow()
window.show()

sys.exit(app.exec_())
