"""functions for moving file and states between ksp instances"""
import shutil
import os
from CosmicKSP.config import config
from CosmicKSP.logging import logger


def sync_quicksave(from_i, to_i):
    """copy the ksp quicksave file from the real game to the sim game"""
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)

    logger.info("Moving quicksave from %s.%s to %s.%s",
        from_instance['NAME'],
        from_instance['GAME_NAME'],
        to_instance['NAME'],
        to_instance['GAME_NAME'],
        )

    for file in ['quicksave.sfs', 'quicksave.loadmeta']:

        from_file = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'], file)
        to_file = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'], file)

        shutil.copy2(from_file, to_file)


def sync_save(from_i, to_i):
    """copy the ksp persistance save from the real game to the sim game """
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)

    logger.info("Moving save from %s.%s to %s.%s",
        from_instance['NAME'],
        from_instance['GAME_NAME'],
        to_instance['NAME'],
        to_instance['GAME_NAME'],
        )

    from_file = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'])
    to_file = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'])

    shutil.copy2(from_file, to_file)


# TODO: this
def sync_ships(from_i, to_i):
    """copy ships from the real ksp to the sim ksp"""
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)
