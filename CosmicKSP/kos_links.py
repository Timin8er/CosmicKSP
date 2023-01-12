"""connection manager for kos"""
from time import sleep, time
from typing import ByteString
import telnetlib
from CosmicKSP.logging import logger
from CosmicKSP.config import config


class KosConnection():
    """manager for the telnet connection to KOS"""

    def __init__(self):
        self.telnet_connection = None
        self.timeout_deadline = 0

        self.open()


    def open(self):
        """open the connection to the KOS telnet port"""
        try:
            self.telnet_connection = telnetlib.Telnet(
                    config['KOS']['HOST'],
                    config['KOS']['PORT'],
                    config['KOS']['TIMEOUT'])

            self.telnet_connection.read_eager()
            self.telnet_connection.write(b'1\n')
            sleep(.2)
            self.telnet_connection.write(b'1\n')
            sleep(.2)
            self.telnet_connection.read_until(b'')

        except Exception:
            logger.exception('Failed to connect to KOS')
            raise


    def send(self, command_str: ByteString):
        """ execute a single kos command """
        if self.timeout_deadline < time():
            self.open()
        self.timeout_deadline = time() + config['KOS']['TIMEOUT']

        self.telnet_connection.write(command_str)
        self.telnet_connection.read_until(b'')

        logger.info('Command Sent: %s', command_str)
        sleep(.2)


    # def stop(self):
    #     """ hault the kos terminal """
    #     if self.timeout_deadline < time():
    #         self.open()
    #     self.telnet_connection.write(telnetlib.IP)


    # def run_script(self, script_instance, *args, volume=1, timeout=0):
    #     """sent the command to run the given script instance"""
    #     args = [f'{volume}:/{script_instance.name}.ks'] + [str(i) for i in list(args)]
    #     com = '", "'.join(args)
    #     command_str = f'runpath("{com}").\n'

    #     self.send(command_str)

    #     if timeout:
    #         sleep(timeout)
    #         self.stop()


    # def kos_upload(self, script_path):
    #     """ upload the given script object to the kos ship """

    #     # write script to temp file
    #     temp_file_path = os.path.join(config['KSP']['DIR'], 'Ships', 'Script', 'temp_upload.ks')

    #     shutil.copyfile(script_path, temp_file_path)

    #     # upload the file
    #     self.send(f'COPYPATH("1:/temp_upload.ks", "0:/{script_instance.name}.ks").')

