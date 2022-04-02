RUNPATH("1:/launchProfile.ks").

LOCAL PITCH_MIN TO 5.
LOCAL SPEED_MIN TO 20.

//////////
// Open the throttle, but save the mono
RCS OFF.
SAS OFF.
WAIT 0.

LOCK THROTTLE TO 1.0.

// Point straight up
LOCAL HEAD TO HEADING(90,90).
LOCK STEERING TO HEAD.

run KStage.

UNTIL SHIP:APOAPSIS > target_ap {
	// Handle steering

	LOCAL SPEED TO SHIP:VELOCITY:SURFACE:MAG.

	IF SPEED < SPEED_MIN {
		SET HEAD TO HEADING(90,90).
	} ELSE {
    LOCAL AP TO SHIP:APOAPSIS.
		Local PITCH TO ROUND(90 - SQRT(AP*pitch_sqrt_mod*0.01) + ((AP*pitch_pow_mod*0.000001)^2) + (AP*pitch_line_mod*0.00001), 1).
		IF PITCH < PITCH_MIN SET PITCH TO PITCH_MIN.

		SET HEAD TO HEADING(90, PITCH).
	}.

  // staging
  LIST ENGINES IN ENGLIST.
  FOR ENG IN ENGLIST {
  	IF ENG:FLAMEOUT = TRUE {
      RUN KStage.
      BREAK.
  	}.
  }.

}.

UNLOCK STEERING.
LOCK THROTTLE TO 0.

// We will want RCS here in case something goes wrong (like fast forward)
RCS ON.
SAS ON.
LOCK THROTTLE TO 0.
WAIT 0. // cant set sasmode on the same tick as sas
SET SASMODE TO "PROGRADE".

WAIT UNTIL SHIP:ALTITUDE > 70000.

// Because we can
PANELS ON.
RADIATORS ON.

// This sets the user's throttle setting to zero to prevent the throttle
// from returning to the position it was at before the script was run.
SET SHIP:CONTROL:PILOTMAINTHROTTLE TO 0.
