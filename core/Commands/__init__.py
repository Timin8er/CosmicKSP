import os
import json

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

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.type = data.get('type', STRING)
        self.value = None

    def encode(self):
        return {
            'name':self.name,
            'type':self.type,
            'value':self.value,
        }

    @classmethod
    def decode(cls, data):
        obj = cls(data)
        return obj


class command():

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.commandText = data.get('command', '')
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



class commandSequence():

    def __init__(self, data={}):
        self.name = data.get('name', '')
        self.content = [command(i) for i in data.get('content', [])]
        self.edited = False


    def append(self, cmd):
        self.content.append(cmd)


    def insert(self, index, cmd):
        self.content.insert(index, cmd)


    def remove(self, cmd):
        if isinstance(cmd, int):
            self.content.pop(cmd)
        else:
            self.content.remove(cmd)


    def encode(self):
        return {
            'name':self.name,
            'content':[i.encode() for i in self.content],
        }


SAVE_FILE = os.path.join(os.path.expanduser('~'), 'Documents', 'CosmicKSP', 'save.json')
if not os.path.isdir(os.path.dirname(SAVE_FILE)):
    os.makedirs(os.path.dirname(SAVE_FILE))

def save_cs(command_sequences):
    data = [i.encode() for i in command_sequences]
    with open(SAVE_FILE, 'w') as outfile:
        json.dump(data, outfile)

def load_cs():
    try:
        with open(SAVE_FILE, 'r') as outfile:
            data = json.load(outfile)
        return [commandSequence(i) for i in data]
    except Exception as e:
        print('ERROR while loading saved Command Sequences')
        print(e)
    return []
