# Script Runner test script
cmd("KSP EXAMPLE")
wait_check("KSP STATUS BOOL == 'FALSE'", 5)
