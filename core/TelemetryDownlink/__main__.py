from . import telemachusDownlink
from CosmicKSP import settings
import datetime

dl = telemachusDownlink(settings.REAL_GAME_INSTANCE['TELEMACHUS'])

while True:
    data = dl.update()
    if data:
        mission_time = datetime.timedelta(seconds=data['v.missionTime'])
        print(f'[{mission_time}] : ', data)
