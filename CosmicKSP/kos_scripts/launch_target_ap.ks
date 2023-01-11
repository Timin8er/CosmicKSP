// Launches a vehicle
PARAMETER target_ap, pitch_line_mod, pitch_pow_mod, pitch_sqrt_mod, pitch_min, speed_min, ship_roll, staging_timing

// target_ap : the target APOAPSIS, in meters
// pitch_line_mod : liniar component of arch
// pitch_pow_mod : squared component of arch
// pitch_sqrt_mod : square root component of arch
// pitch min : minimum pitch
// speed_min : minimum speed before turning
// ship_roll : roll orientation of the ship during launch
// staging_timing : list of delays for dual staging, 0 means single stage event 

LOCAL staging_timing_index TO 1. // starts at 1 because 0 is hard coded
LOCAL head TO HEADING(90,90,ship_roll).

////////// Launch //////////
// Open the throttle, but save the mono
RCS OFF.
SAS OFF.
WAIT 0.

LOCK THROTTLE TO 1.0.
LOCK STEERING TO head.

run dual_stage_delay(staging_timing[0]).

////////// Maintain Heading //////////
UNTIL SHIP:APOAPSIS > target_ap {
	// Handle steering

	LOCAL SPEED TO SHIP:VELOCITY:SURFACE:MAG.

	IF SPEED >= speed_min {
    	LOCAL AP TO SHIP:APOAPSIS.
		Local pitch TO ROUND(90 - SQRT(AP*pitch_sqrt_mod*0.01) + ((AP*pitch_pow_mod*0.000001)^2) + (AP*pitch_line_mod*0.00001), 1).
		
		IF pitch < pitch_min SET pitch TO pitch_min.

		SET head TO HEADING(90, pitch, ship_roll).
	}.

  // staging
  LIST ENGINES IN ENGLIST.
  FOR ENG IN ENGLIST {
  	IF ENG:FLAMEOUT = TRUE {
      RUN dual_stage_delay(staging_timing[staging_timing_index]).
	  set staging_timing_index TO staging_timing_index + 1.
      BREAK.
  	}.
  }.

}.

////////// Coast //////////
UNLOCK STEERING.
SET SHIP:CONTROL:PILOTMAINTHROTTLE TO 0.
LOCK THROTTLE TO 0.

// We will want RCS here in case something goes wrong (like fast forward)
SAS ON.
WAIT 0. // cant set sasmode on the same tick as sas
SET SASMODE TO "PROGRADE".

WAIT UNTIL SHIP:ALTITUDE > BODY:ATM:HEIGHT.

UNLOCK THROTTLE.