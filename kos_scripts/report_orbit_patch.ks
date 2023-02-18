PARAMETER orbit_index, after_node.

local o to SHIP:ORBIT.

if after_node {
    set o to NEXTNODE:ORBIT.
}.

local total_patches to 0.
local oi to o.

Until oi:HASNEXTPATCH = False {
    set oi to oi:NEXTPATCH.
    set total_patches to total_patches + 1.
}.

FROM {local i is orbit_index.} UNTIL i = 0 STEP {set i to i-1.} DO {
  set o to o:NEXTPATCH.
}.

print("Orbit Index: " + orbit_index + "/" + total_patches).
print("Name: " + o:NAME).
print("Apoapsis: " + o:APOAPSIS).
print("Periapsis: " + o:PERIAPSIS).
print("Inclination: " + o:INCLINATION).
print("Eccentricity: " + o:ECCENTRICITY).
