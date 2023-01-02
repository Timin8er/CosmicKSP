# Script Runner test script
cmd("COSMICKSP EXAMPLE")
wait_check("COSMICKSP STATUS BOOL == 'FALSE'", 5)
