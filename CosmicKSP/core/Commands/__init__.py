import os
import json

FLOAT = 0
STRING = 1
ENUM = 2

COMMANDS = [
    {
        'name':'Test',
        'description':'Test command',
        'commandText':'set LOL to list("{str}", {flt}, "{state}")',
        'arguements':[
            {
                'name':'Str',
                'key':'str',
                'type':STRING,
                'value':'LOL'
            },
            {
                'name':'Flt',
                'key':'flt',
                'type':FLOAT,
                'value':3.1459
            },
            {
                'name':'State',
                'key':'state',
                'type':ENUM,
                'options':['ON', 'OFF'],
                'value':'ON'
            }
        ],
    },
    {
        'name':'Stage',
        'description':'space bar goes to space.',
        'commandText':'STAGE',
        'arguements':[],
    },
    {
        'name':'Set SAS',
        'description':'Set the state of SAS',
        'commandText':'SAS {state}',
        'arguements':[
            {
                'name':'State',
                'key':'state',
                'type':ENUM,
                'options':['ON', 'OFF'],
                'value':'ON'
            }
        ],
    }
]


class commandArgument():

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.key = data.get('key', '')
        self.type = data.get('type', STRING)
        self.value = data.get('value', None)
        self.options = data.get('options', [])

    def encode(self):
        return {
            'name':self.name,
            'key':self.key,
            'type':self.type,
            'value':self.value,
            'options':self.options,
        }


class command():

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.commandText = data.get('commandText', '')
        self.description = data.get('description', '')
        self.arguements = [commandArgument(i) for i in data.get('arguements', [])]
        self.edited = False

    def encode(self):
        return {
            'name':self.name,
            'commandText':self.commandText,
            'description':self.description,
            'arguements':[i.encode() for i in self.arguements],
        }

    def kosString(self):
        if len(self.arguements):
            return self.commandText.format(**{i.key:i.value for i in self.arguements})
        else:
            return self.commandText



class commandSequence():

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.commands = [command(i) for i in data.get('commands', [])]
        self.folder = data.get('folder', '')
        self.edited = False


    def append(self, cmd):
        self.commands.append(cmd)


    def insert(self, index, cmd):
        self.commands.insert(index, cmd)


    def remove(self, cmd):
        if isinstance(cmd, int):
            self.commands.pop(cmd)
        else:
            self.commands.remove(cmd)


    def encode(self):
        return {
            'name':self.name,
            'folder':self.folder,
            'commands':[i.encode() for i in self.commands],
        }


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
