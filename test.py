import json

class VerilogName:
    def __init__(self, name, type):
        self.name = name;
        self.type = type;

    def __str__(self):
        info = { 'name': self.name, 'type': self.type }
        return json.dumps(info)


class VerilogModule:

    def __init__(self):
        self.name = 'default';
        self.names = [];

    def __init__(self, name):
        self.name = name;
        self.names = [];

    def addName(self, name):
        self.names.append(name);

    def __str__(self):
        info = { 'name': self.name, 'names': self.names }
        return json.dumps(info)

module1 = VerilogModule('module1')

name1 = VerilogName('asdf', 0)

module1.addName(name1)


print(module1)
