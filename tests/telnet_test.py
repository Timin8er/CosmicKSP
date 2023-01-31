"""the controll loops for the commands relay pipeline"""
from typing import ByteString
import socket
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config

logger = get_logger(name='CosmicKSP_Commanding')
logger.setLevel(config['logging_level'])



def main():
    """main"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 5410))
    s.listen(1)
    c,remote=s.accept()

    while True:
        data = c.recv(4096)
        logger.info(data)


if __name__ == '__main__':
    main()
