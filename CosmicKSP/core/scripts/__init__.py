import os
import shutil

MY_PATH = os.path.dirname(__file__)


def copyToGame(instance):
    dest = os.path.join(instance['DIR'], 'Ships', 'Script')

    shutil.copy(MY_PATH, dest)  # dst can be a folder; use shutil.copy2() to preserve timestamp


def copyFromGame(instance):
    dest = os.path.join(instance['DIR'], 'Ships', 'Script')

    shutil.copy(dest, MY_PATH)
