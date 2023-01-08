"""the controll loops for the commands relay pipeline"""
import time
from typing import Dict
from PyQt5.QtCore import QThread, pyqtSignal
from CosmicKSP.logging import logger
from CosmicKSP.kos_links import KosConnection


class TelemetryRelayThread(QThread):
    """QThread loops through telemetry"""

    telemReport = pyqtSignal(dict)
    signalStatus = pyqtSignal(int)

    def run(self):
        commands_loop()



def commands_loop():
    """loop of recieving telemetry"""
    logger.info('Commands Relay Starting')
    kos = KosConnection()

    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            logger.info('Commands Relay Stopped: Keyboard Interupt')
            break
