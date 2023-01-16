"""functions for managing the ksp games"""
import sys
from CosmicKSP.logging import logger
from . import save_management

def main():
    """run a function based on system arguements"""
    try:
        match sys.argv:
            case [script]:
                logger.error('not enough arguements')

            case [script, 'sync']:
                save_management.sync_quicksave('REAL', 'SIM')

            case [script, 'sync', from_save, to_save]:
                save_management.sync_quicksave(from_save, to_save)

            case [script, 'copysave']:
                save_management.sync_save('REAL', 'SIM')

            case [script, 'copysave', from_save, to_save]:
                save_management.sync_save(from_save, to_save)

            case [script, 'copyships']:
                save_management.sync_ships('REAL', 'SIM')

            case [script, 'copyships', from_save, to_save]:
                save_management.sync_ships(from_save, to_save)

            case _:
                logger.error('invalid arguements')

    except Exception:
        logger.exception('Main Failed')


if __name__ == "__main__":
    main()
