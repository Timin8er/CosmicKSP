set node_time to TIME:SECONDS + ETA:APOAPSIS.
set burnapsis to APOAPSIS.

print "Setting up maneuver node. ETA=" + (node_time - TIME:SECONDS).
LOCAL burn to NODE(node_time, 0,0,0).

add burn.

LOCAL v_old to sqrt(BODY:MU * (2/(burnapsis+BODY:RADIUS) - 1/SHIP:OBT:SEMIMAJORAXIS)).
LOCAL v_new to sqrt(BODY:MU * (2/(burnapsis+BODY:RADIUS) - 1/(BODY:RADIUS+burnapsis))).

set burn:PROGRADE to v_new-v_old.
