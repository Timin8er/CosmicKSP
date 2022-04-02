IF DEFINED staging_timing {

  LOCAL delay TO staging_timing[staging_timing_index].

  // if delay is 0, only stage once.
  if delay = 0 {
    STAGE.

  // if not, stage twice with the given delay.
  } ELSE {
    STAGE.
    WAIT delay.
    STAGE.
  }.

  // increment the stage index if we're not at the end.
  IF staging_timing_index < staging_timing:LENGTH {
    SET staging_timing_index TO staging_timing_index + 1.
  }.

} ELSE {
  STAGE.
}
