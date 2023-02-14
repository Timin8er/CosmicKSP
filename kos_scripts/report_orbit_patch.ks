PARAMETER orbit_index, after_node.

local o to SHIP:ORBIT.
if node_index != -1 {
    ALLNODES[node_index]
}

print("Orbit Index: " + orbit_index + "/" + SHIP:PATCHES:LENGTH).
print("Name: " + o:NAME).
print("Apoapsis: " + o:APOAPSIS).
print("Periapsis: " + o:PERIAPSIS).
print("Inclination: " + o:INCLINATION).
print("Eccentricity: " + o:ECCENTRICITY).
