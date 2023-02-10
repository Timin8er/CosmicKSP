PARAMETER orbit_index.

local o TO SHIP:PATCHES[orbit_index].

print("Orbit Index: " + orbit_index + "/" + SHIP:PATCHES:LENGTH).
print("Name: " + o:NAME).
print("Apoapsis: " + o:APOAPSIS).
print("Periapsis: " + o:PERIAPSIS).
print("Inclination: " + o:INCLINATION).
print("Eccentricity: " + o:ECCENTRICITY).
