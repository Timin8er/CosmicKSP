FLOAT = 0
STRING = 1
ENUM = 2

COMMANDS = [
    {
        'name':'Stage',
        'description':'space bar goes to space.',
        'command':'stage',
        'arguements':[],
    }
]


class commandArgument():

    def __init__(self, arg={}):
        self.name = arg.get('name', '')
        self.type = arg.get('type', STRING)
        self.value = None


class command():

    def __init__(self, cmd={}):
        self.name = cmd.get('name', '')
        self.commandText = cmd.get('command', '')
        self.description = cmd.get('description', '')
        self.arguements = [commandArgument(arg) for arg in cmd.get('arguements', [])]
