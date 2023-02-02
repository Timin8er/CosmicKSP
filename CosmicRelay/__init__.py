"""These are the processes for running the command and telemetrie relays from openc3 to KSP"""
import sys
import os


def main():
    """opens two new terminals and runs the uplink and downlink in each"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelay_Telemetry')
        os.system('start cmd.exe /K CosmicRelay_Commanding')

    else:
        os.system('gnome-terminal --tab --title="CosmicKSP Telemetry" -- CosmicRelay_Telemetry')
        os.system('gnome-terminal --tab --title="CosmicKSP Commanding" -- CosmicRelay_Commanding')


if __name__ == '__main__':
    main()
