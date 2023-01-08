"""connection manager for kos"""
from time import sleep, time
import telnetlib
import os
from PyQt5.QtCore import QObject, pyqtSignal
from CosmicKSP.logging import logger


class KosConnection(QObject):
    """manager for the telnet connection to KOS"""

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
            self._connection = telnetlib.Telnet(
                    self.settings['HOST'],
                    self.settings['PORT'],
                    self.settings['TIMEOUT'])

            self._connection.read_eager()
            self._connection.write(b'1\n')
            sleep(.2)
            self._connection.write(b'1\n')
            sleep(.2)
            self._connection.read_until(b'')

        except Exception:
            logger.exception('Failed to connect to KOS')


    def send_command_str(self, command_str):
        """ execute a single kos command """
        if self._time_deadline < time():
            self.open()

        if not command_str.endswith('.'):
            command_str += '.'

        self._time_deadline = time() + self.settings['TIMEOUT']
        self._connection.write(f'{command_str}\n'.encode())
        self._connection.read_until(b'')
        self.commandSent.emit(command_str)
        logger.info('Command Sent: %s', command_str)
        sleep(.2)


    def stop(self):
        """ hault the kos terminal """
        if self._time_deadline < time():
            self.open()
        self._connection.write(telnetlib.IP)
        self.commandSent.emit(str(telnetlib.IP))


    def run_script(self, script_instance, *args, volume=1, timeout=0):
        """sent the command to run the given script instance"""
        args = [f'{volume}:/{script_instance.name}.ks'] + [str(i) for i in list(args)]
        com = '", "'.join(args)
        command_str = f'runpath("{com}").\n'

        self.send_command_str(command_str)

        if timeout:
            sleep(timeout)
            self.stop()


    def kos_upload(self, script_instance):
        """ upload the given script object to the kos ship """

        # write script to temp file
        temp_file_path = os.path.join(self.settings['DIR'], 'Ships', 'Script', 'temp_upload.ks')

        with open(temp_file_path, 'w', encoding="utf-8") as file:
            file.write(script_instance.text)

        # upload the file
        self.send_command_str(f'COPYPATH("1:/temp_upload.ks", "0:/{script_instance.name}.ks").')
