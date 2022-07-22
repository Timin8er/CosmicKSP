from . import CosmosDownlink
from CosmicKSP import settings

dl = CosmosDownlink(settings.REAL_GAME_INSTANCE)

while True:
    data = dl.listen()
    if data:
        print(data)
