import os

SCRIPT_STORAGE_FILE = os.path.join(os.path.dirname(__file__), 'scripts.json')

REAL_GAME_INSTANCE = {
    'DIR':r'C:\KSP\CosmicKSP',
    'HOST':'127.0.0.1',
    'PORT':5410,
    'TIMEOUT':10,
    'TELEMACHUS':{
        'HOST':'127.0.0.1',
        'PORT':8085,
        'FREQUENCY':500,
    }
}

SIM_GAME_INSTANCE = {
    'DIR':r'C:\KSP\CosmicKSP_Sim',
    'HOST':'127.0.0.1',
    'PORT':5411,
    'TIMEOUT':10,
    'TELEMACHUS':{
        'HOST':'127.0.0.1',
        'PORT':8085,
        'FREQUENCY':500,
    }
}

COSMOS_IP = '127.0.0.1'
COSMOS_PORT = 1248


# PRINT_TRANSLATION = {
#     'v.missionTime':'{:.3f} ',
#     'v.altitude':'{:.3f} ',
#     'r.resource[LiquidFuel]':'{:.3f}'
# }
#
#
# STRING_TRANSLATION = {
#     'v.missionTime':'{:20}',
#     'v.altitude':'{:20}',
#     'r.resource[LiquidFuel]':'{:20}'
# }
