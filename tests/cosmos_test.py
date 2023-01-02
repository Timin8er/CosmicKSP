from CosmicKSP.logging import logger
from CosmicKSP.core import cosmos_links

def main():
    """run the cosmos telemetry downlink injector"""
    try:
        cosmos_links.cosmos_telemetry_loop()

    except Exception as e:
        logger.exception('Main Failed')


if __name__ == "__main__":
    main()