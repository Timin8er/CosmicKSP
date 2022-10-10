import logging

LOGGING_LEVEL = logging.DEBUG

REAL_GAME_INSTANCE = {
    'DIR':r'C:\KSP\CosmicKSP',
    'GAME_NAME': 'default',
    'TELEMACHUS':{
        'HOST':'127.0.0.1',
        'PORT':8085,
        'FREQUENCY':500,
    },
    'KOS': {
        'HOST':'127.0.0.1',
        'PORT':5410,
        'TIMEOUT':10,
    },
    'COSMOS': {
        'HOST': 'cosmos.timin8er.com',
        'PORT': 1248,
    }
}

SIM_GAME_INSTANCE = {
    'DIR':r'C:\KSP\CosmicKSP_Sim',
    'GAME_NAME': 'default',
    'TELEMACHUS':{
        'HOST':'127.0.0.1',
        'PORT':8086,
        'FREQUENCY':500,
    },
    'KOS': {
        'HOST':'127.0.0.1',
        'PORT':5411,
        'TIMEOUT':10,
    },
    'COSMOS': {
        'HOST': 'cosmos.timin8er.com',
        'PORT': 1248,
    }
}
