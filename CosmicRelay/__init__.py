"""These are the processes for running the command and telemetrie relays from openc3 to KSP"""
import sys
import os
# from CosmicKSP.logging import logger
# from CosmicKSP.config import config
# from CosmicRelay.telemetry_relay import telemetry_loop
# from CosmicRelay.commands_relay import commands_loop

# logger.setLevel(config['LOGGING_LEVEL'])



def main():
    """opens two new terminals and runs the uplink and downlink in each"""
    if sys.platform == "win32":
        os.system('start cmd.exe /K CosmicRelayDownlink"')
        os.system('start cmd.exe /K CosmicRelayUplink"')

    else:
        os.system('gnome-terminal --tab --title=TelemachusRelayDownlink -- CosmicRelayDownlink')
        os.system('gnome-terminal --tab --title=TelemachusRelayUplink -- CosmicRelayUplink')


# def up_main():
#     """run the commands uplink relay"""
#     try:
#         commands_loop()

#     except Exception:
#         logger.exception('Main Failed')


# def down_main():
#     """run the telemetry downlink relay"""
#     try:
#         telemetry_loop()

#     except Exception:
#         logger.exception('Main Failed')


if __name__ == '__main__':
    main()
