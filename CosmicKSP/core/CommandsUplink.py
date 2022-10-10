from time import sleep, time
import telnetlib
import os
from PyQt5.QtCore import QObject, pyqtSignal

import logging
logger = logging.getLogger('CosmicKSP')


class kosConnection(QObject):

    commandSent = pyqtSignal(str)

    def __init__(self, instance):
        super().__init__()
        self.settings = instance
        self._connection = None
        self._time_deadline = 0

        try:
            self.open()
        except Exception as e:
            logger.critical(str(e))


    def open(self):
        self._connection = telnetlib.Telnet(self.settings['KOS']['HOST'], self.settings['KOS']['PORT'], self.settings['KOS']['TIMEOUT'])

        self._connection.read_eager()
        self._connection.write(b'1\n')
        sleep(.2)
        self._connection.write(b'1\n')
        sleep(.2)
        self._connection.read_until(b'')


    def sendCommandStr(self, command_str):
        """ execute a single kos command """
        if self._time_deadline < time():
            self.open()

        if not command_str.endswith('.'):
            command_str += '.'

        self._time_deadline = time() + 15
        self._connection.write(f'{command_str}\n'.encode())
        self._connection.read_until(b'')
        self.commandSent.emit(command_str)
        sleep(.2)


    def stop(self):
        """ hault the kos terminal """
        if self._time_deadline < time():
            self.open()
        _ = self._connection.write(telnetlib.IP)
        self.commandSent.emit(str(telnetlib.IP))


    def kosRunScript(self, script_instance, *args, volume=1, timeout=0):
        """  """
        args = [f'{volume}:/{script_instance.name}.ks'] + [str(i) for i in list(args)]
        com = '", "'.join(args)
        command_str = f'runpath("{com}").\n'
        self.sendCommandStr(command_str)

        if timeout:
            sleep(timeout)
            self.ks_stop()


    def kosUpload(self, script_instance):
        """ upload the given script object to the kos ship """

        # write script to temp file
        temp_file = os.path.join(self.settings['DIR'], 'Ships', 'Script', 'temp_upload.ks')

        with open(temp_file, 'w') as f:
            f.write(script_instance.text)

        # upload the file
        self.sendCommandStr(f'COPYPATH("1:/temp_upload.ks", "0:/{script_instance.name}.ks").')
