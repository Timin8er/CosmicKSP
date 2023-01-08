local name is SHIP:SHIPNAME.
set name to name:replace(" ", "").

print("Initializing "+name).
RUNPATH("0:/init_files/"+name+".init.ks").
