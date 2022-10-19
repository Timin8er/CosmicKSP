import os
import json
from PyQtDataFramework.Core.Logging import logger
from PyQtDataFramework.Core.Models import BaseModel
from PyQtDataFramework.Core import Fields


class KosCommand(BaseModel):

    __cmd_name__ = None

    def __str__(self):
        inputs = [getattr(self, f.key) for f in self.fields()]
        return f'{self.__cmd_name__}({",".join(inputs)}).'


class CmdSetSAS(KosCommand):

    __cmd_name__ = 'SAS'

    state = Fields.enumField(['ON', 'OFF'], default='ON', display_name='ON/OFF')

    def __str__(self):
        return f'SAS {self.state}.'


class CmdStage(KosCommand):

    __cmd_name__ = 'Stage':

    def __str__(self):
        return 'stage.'




class commandSequence(BaseModel):

    name = Fields.charfield()
    commands = Fields.listField(KosCommand)


SAVE_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'CosmicKSP', 'save.json')
if not os.path.isdir(os.path.dirname(SAVE_FILE)):
    os.makedirs(os.path.dirname(SAVE_FILE))

def save_cs(command_sequences):
    data = [i.encode() for i in command_sequences]
    with open(SAVE_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def load_cs():
    try:
        with open(SAVE_FILE, 'r') as outfile:
            data = json.load(outfile)
        return [commandSequence(i) for i in data]

    except Exception as e:
        logger.error(str(e))
    return []
