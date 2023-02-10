// This script executes the next manuever node
PARAMETER staging_timing.

SAS OFF.

LOCAL next_node to nextnode.

print "Node in: " + round(next_node:eta) + " s, DeltaV: " + round(next_node:deltav:mag) + " m/s".

LOCAL max_acc to ship:maxthrust/ship:mass.

LOCAL burn_duration to next_node:deltav:mag/max_acc.
print "Crude Estimated burn duration: " + round(burn_duration) + "s".


wait until next_node:eta <= (burn_duration/2 + 60).

LOCAL np to next_node:deltav. //points to node, don't care about the roll direction.
LOCK steering to np.

//now we need to wait until the burn vector and ship's facing are aligned
wait until vang(np, ship:facing:vector) < 0.25.

//the ship is facing the right direction, let's wait for our burn time
wait until next_node:eta <= (burn_duration/2).

print("begining burn").

//we only need to lock throttle once to a certain variable in the beginning of the loop, and adjust only the variable itself inside it
LOCAL tset to 0.
LOCK throttle to tset.

LOCAL done to False.
//initial deltav
LOCAL dv0 to next_node:deltav.
until done
{
    //recalculate current max_acceleration, as it changes while we burn through fuel
    set max_acc to ship:maxthrust/ship:mass.

    //throttle is 100% until there is less than 1 second of time left to burn
    //when there is less than 1 second - decrease the throttle linearly
    set tset to min(next_node:deltav:mag/max_acc, 1).

    //here's the tricky part, we need to cut the throttle as soon as our next_node:deltav and initial deltav start facing opposite directions
    //this check is done via checking the dot product of those 2 vectors
    if vdot(dv0, next_node:deltav) < 0
    {
        print "End burn, remain dv " + round(next_node:deltav:mag,1) + "m/s, vdot: " + round(vdot(dv0, next_node:deltav),1).
        LOCK throttle to 0.
        break.
    }

    //we have very little left to burn, less then 0.1m/s
    if next_node:deltav:mag < 0.1
    {
        print "Finalizing burn, remain dv " + round(next_node:deltav:mag,1) + "m/s, vdot: " + round(vdot(dv0, next_node:deltav),1).
        //we burn slowly until our node vector starts to drift significantly from initial vector
        //this usually means we are on point
        wait until vdot(dv0, next_node:deltav) < 0.5.

        LOCK throttle to 0.
        print "End burn, remain dv " + round(next_node:deltav:mag,1) + "m/s, vdot: " + round(vdot(dv0, next_node:deltav),1).
        set done to True.
    }
}
UNLOCK steering.
UNLOCK throttle.
wait 1.

//we no longer need the maneuver node
remove next_node.

//set throttle to 0 just in case.
SET SHIP:CONTROL:PILOTMAINTHROTTLE TO 0.
