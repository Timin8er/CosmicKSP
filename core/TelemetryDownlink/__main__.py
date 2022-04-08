from . import tlmDownlink, translate
from CosmicKSP import settings
import pprint

dl = tlmDownlink(settings.TELEMACHUS_HOST, settings.TELEMACHUS_PORT, settings.TELEMACHUS_FREQUENCY)
for key in settings.TELEMETRY_SUBSCIPTIONS:
    dl.subscribe(key)

while True:
    data = dl.update()
    if data:
        print(translate(data, settings.PRINT_TRANSLATION))
    # pprint.pprint(d)
