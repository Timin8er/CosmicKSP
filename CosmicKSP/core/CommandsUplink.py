""""""
from PyQtDataFramework.Core.Logging import logger
from time import sleep, time
import telnetlib
import os
from PyQt5.QtCore import QObject, pyqtSignal

COMMAND_TIMEOUT = 15


class KosConnection(QObject):

    commandSent = pyqtSignal(str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self._connection = None
        self._time_deadline = 0

        self.open()


    def open(self):
        """open the connection to the KOS telnet port"""
        try:
            self._connection = telnetlib.Telnet(self.settings['HOST'], self.settings['PORT'], self.settings['TIMEOUT'])

            self._connection.read_eager()
            self._connection.write(b'1\n')
            sleep(.2)
            self._connection.write(b'1\n')
            sleep(.2)
            self._connection.read_until(b'')

        except Exception as ex:
            logger.exception('Failed to connect to KOS')


    def sendCommandStr(self, command_str):
        """ execute a single kos command """
        if self._time_deadline < time():
            self.open()

        if not command_str.endswith('.'):
            command_str += '.'

        self._time_deadline = time() + COMMAND_TIMEOUT
        self._connection.write(f'{command_str}\n'.encode())
        self._connection.read_until(b'')
        self.commandSent.emit(command_str)
        logger.info('Command Sent: {}' % command_str)
        sleep(.2)


    def stop(self):
        """ hault the kos terminal """
        if self._time_deadline < time():
            self.open()
        _ = self._connection.write(telnetlib.IP)
        self.commandSent.emit(str(telnetlib.IP))


    def kosRunScript(self, script_instance, *args, volume=1, timeout=0):
        """sent the command to run the given script instance"""
        args = [f'{volume}:/{script_instance.name}.ks'] + [str(i) for i in list(args)]
        com = '", "'.join(args)
        command_str = f'runpath("{com}").\n'

        self.sendCommandStr(command_str)

        if timeout:
            sleep(timeout)
            self.stop()


    def kosUpload(self, script_instance):
        """ upload the given script object to the kos ship """

        # write script to temp file
        temp_file = os.path.join(self.settings['DIR'], 'Ships', 'Script', 'temp_upload.ks')

        with open(temp_file, 'w') as f:
            f.write(script_instance.text)

        # upload the file
        self.sendCommandStr(f'COPYPATH("1:/temp_upload.ks", "0:/{script_instance.name}.ks").')
