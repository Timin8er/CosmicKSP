"""functions for managing the ksp games"""
import sys
import os
from CosmicKSP.logging import get_logger
from CosmicKSP.config import config
from . import save_management

SAVES_DIR = os.path.expanduser(os.path.join(config['ksp']['dir'], 'saves', config['ksp']['save']))

def main():
    """run a function based on system arguements"""
    logger = get_logger(name='CosmicKSP_Commanding')
    logger.setLevel(config['logging_level'])

    match sys.argv:
        case [_]:
            logger.error('not enough arguements')

        case [_, 'sync']:
            save_management.sync_quicksave('REAL', 'SIM')

        case [_, 'sync', from_save, to_save]:
            save_management.sync_quicksave(from_save, to_save)

        case [_, 'copysave']:
            save_management.sync_save('REAL', 'SIM')

        case [_, 'copysave', from_save, to_save]:
            save_management.sync_save(from_save, to_save)

        case [_, 'copyships']:
            save_management.sync_ships('REAL', 'SIM')

        case [_, 'copyships', from_save, to_save]:
            save_management.sync_ships(from_save, to_save)

        case _:
            logger.error('invalid arguements')


if __name__ == "__main__":
    main()
