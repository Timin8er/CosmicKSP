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


DEPENDANCIES = {
    'launch_target_ap': [
        'dual_stage_delay',
        'create_node_circularise_at_apoapsis',
        'execute_next_manuever_node']
}


# runpath("0:/launch_target_ap.ks", 100000, 35, 40, 16, 10, 20, 0, list(0,0,0,0,2)).
# copypath("0:/dual_stage_delay.ks", "1:/dual_stage_delay.ks").
# runpath("0:/manuevers/create_node_circularise_at_apoapsis.ks").
# runpath("0:/manuevers/execute_next_manuever_node.ks").
# 
