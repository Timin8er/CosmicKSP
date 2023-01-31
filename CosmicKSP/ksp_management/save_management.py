"""functions for moving file and states between ksp instances"""
from typing import ByteString
import shutil
import os
from CosmicKSP.config import config


def sync_quicksave(from_i, to_i):
    """copy the ksp quicksave file from the real game to the sim game"""
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)

    for file in ['quicksave.sfs', 'quicksave.loadmeta']:

        from_file = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'], file)
        to_file = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'], file)

        shutil.copy2(from_file, to_file)


def sync_save(from_i, to_i):
    """copy the ksp persistance save from the real game to the sim game """
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)

    from_file = os.path.join(from_instance['DIR'], 'saves', from_instance['GAME_NAME'])
    to_file = os.path.join(to_instance['DIR'], 'saves', to_instance['GAME_NAME'])

    shutil.copy2(from_file, to_file)


# TODO: this
def sync_ships(from_i, to_i):
    """copy ships from the real ksp to the sim ksp"""
    from_instance = config.getInstance(from_i)
    to_instance = config.getInstance(to_i)
