"""package for managing the kos script volumes"""
import os
import shutil

MY_PATH = os.path.dirname(__file__)


def copy_script_to_game(instance):
    """copy a script to the ksp volume"""
    dest = os.path.join(instance['DIR'], 'Ships', 'Script')

    shutil.copy(MY_PATH, dest)  # dst can be a folder; use shutil.copy2() to preserve timestamp


def copy_script_from_game(instance):
    """copy a script from the game instance"""
    dest = os.path.join(instance['DIR'], 'Ships', 'Script')

    shutil.copy(dest, MY_PATH)
