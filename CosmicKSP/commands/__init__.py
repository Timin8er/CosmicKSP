"""command translation classes"""
from typing import Dict, ByteString
from pyqt_data_framework.data_models import Model, fields


def telem_openc3_to_telemechus(s_telem: ByteString) -> Dict:
    """translate the OpenC3 command to KOS command"""
    return {}


class KosCommand(Model):
    """base KOS command"""

    __cmd_name__ = None

    def __str__(self):
        inputs = [getattr(self, f.key) for f in self.fields()]
        return f'{self.__cmd_name__}({",".join(inputs)}).'


class CmdSetSAS(KosCommand):
    """KOS command to set the SAS"""

    __cmd_name__ = 'SAS'

    state = fields.EnumField(['ON', 'OFF'], default='ON', display_name='ON/OFF')

    def __str__(self):
        return f'SAS {self.state}.'


class CmdStage(KosCommand):
    """KOS command to stage"""

    __cmd_name__ = 'Stage'

    def __str__(self):
        return 'stage.'


class CommandSequence(Model):
    """list of commands"""

    name = fields.StringField()
    commands = fields.ListField(KosCommand)
