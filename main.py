import re
import collections
import os, sys
import json

class VerilogModule:
    def __init__(self):
        self.name = 'default'
        self.inputs = [];
        self.outputs = [];
        self.wires = [];
        self.inouts = [];

    def __init__(self, name):
        self.name = name
        self.inputs = [];
        self.outputs = [];
        self.wires = [];
        self.inouts = [];

    def addInput(self, input):
        self.inputs.append(input)

    def addInout(self, name):
        self.inouts.append(name)

    def addOutput(self, name):
        self.outputs.append(name)

    def addWire(self, name):
        self.wires.append(name)

    def __str__(self):
        info = {
            'name': self.name,
            'inputs': self.inputs,
            'inouts': self.inouts,
            'outputs': self.outputs,
            'wires': self.wires
        }
        return json.dumps(info)

def _get_only_name(text):
    x = re.sub('[\(\[].*?[\)\]]', '', text)
    x = re.sub(' +', ' ', x)
    x = re.sub(';', '', x)
    return x.strip()

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def _find_modules_in(filepath):
    modules = []; module = '';
    do_read_module = False;
    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            if do_read_module:
                module += line

            match = re.compile(r'\bmodule\b | \bendmodule\b', flags=re.I | re.X)
            res = match.search(line)
            if res:
                if res.group() == 'module':
                    do_read_module = True
                    module += line
                elif res.group() == 'endmodule':
                    do_read_module = False
                    modules.append(module)
                    module = ''
            line = file.readline()
    return modules

def _parse_file(filepath):
    name = ''; newMod = VerilogModule(''); modules = [];

    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            key, match = _parse_line(line)

            if key == 'module':
                name = _get_only_name(match.group(key))
                newMod = VerilogModule(name)
                modules.append(newMod)
            if key == 'input':
                name = _get_only_name(match.group(key))
                newMod.addInput(name);
            if key == 'inout':
                name = _get_only_name(match.group(key))
                newMod.addInout(name);
            if key == 'output':
                name = _get_only_name(match.group(key))
                newMod.addOutput(name);
            if key == 'wire':
                name = _get_only_name(match.group(key))
                newMod.addWire(name);

            line = file.readline()
    return modules

rx_dict = {
    'input'  : re.compile(r'input(?P<input>.*;)'),
    'output' : re.compile(r'output(?P<output>.*;)'),
    'inout'  : re.compile(r'inout(?P<inout>.*;)'),
    'wire'   : re.compile(r'wire(?P<wire>.*;)'),
    'module' : re.compile(r'\bmodule\b(?P<module>.*\w)')
}

if __name__ == '__main__':
    modules = []

    # filepath = 'tx_handler_bad.phy.v'
    # filepath = 'sample01.v'
    filepath = 'test_multiple_modules.phy.v'
    modules = _parse_file(filepath);

    for mod in modules:
        print(mod)



    # data = map(lambda x: x.lower(), data)
    # repeated = [item for item, count in collections.Counter(data).items() if count > 1]
    # print('List of repeated names:')
    # print(repeated)

    # found_modules = _find_modules_in(filepath)
    #
    # for module in found_modules:
    #     print(module)
    #     # for line in module:
    #         # print(_find_key_names(line))

    # res = re.compile(r'\bmodule\b | \bendmodule\b', flags=re.I | re.X)
    # print(res.search('asdfdsf A ('))

    # input = open(filepath)
    # output = open(filepath+'_fixed', 'w')
    #
    # for s in input.xreadlines():
    #     new_str = s;
    #     for x in repeated:
    #         if x in new_str:
    #             new_str = re.sub(r'\b'+x+r'\b', '/______GENERATED_________'+x , new_str)
    #     output.write(new_str)
    #
    # input.close()
    # output.close()
