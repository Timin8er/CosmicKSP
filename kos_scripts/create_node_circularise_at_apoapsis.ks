// Adds a manuever node at apoapsis that circularises the orbit

print "Setting up maneuver node to circularise at APOAPSIS. ETA=" + ETA:APOAPSIS.

local node_time to TIME:SECONDS + ETA:APOAPSIS.

local burnapsis to APOAPSIS + BODY:RADIUS.
LOCAL v_old to sqrt(BODY:MU * (2/(burnapsis) - 1/SHIP:OBT:SEMIMAJORAXIS)).
LOCAL v_new to sqrt(BODY:MU * (2/(burnapsis) - 1/(burnapsis))).

// NODE(time, radial, normal, prograde)
LOCAL burn to NODE(node_time, 0, 0, v_new-v_old).
add burn.
