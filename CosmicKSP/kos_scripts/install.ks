parameter root_file.

SET _dep TO LIST().
_dep:ADD(LIST("launch", "KStage")).
_dep:ADD(LIST("launch_target_ap", "dual_stage_delay")).
_dep:ADD(LIST("manuevers/circularise_at_apoapsis", "manuevers/execute_next_manuever_node")).
_dep:ADD(LIST("manuevers/circularise_at_apoapsis", "manuevers/execute_next_manuever_node")).

// this function recursively loops throught the dependancy tree and loads scripts into the kos disk.
function recursive_dependancy_load {
  parameter file.
  print "installing: " + file.

  LOCAL filepath TO "0:/" + file + ".ks".
  COPYPATH( filepath, "1:/" ).

  FOR f IN _dep {
    IF f[0] = file {
      FOR dep IN f:SUBLIST(1, f:LENGTH -1) {
        recursive_dependancy_load(dep).
      }
    }
  }
}

recursive_dependancy_load(root_file).
