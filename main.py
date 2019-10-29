import re
import collections
import os, sys, getopt
import json

# Definition of type:
#     input = 0 | output = 1 | inout = 2 | wire = 3

class VerilogName:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class VerilogModule:

    def __init__(self):
        self.name = 'default'
        self.names = []
        self.namesToChange = []

    def __init__(self, name):
        self.name = name
        self.names = []
        self.namesToChange = []

    def addName(self, name):
        self.names.append(name)

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
            elif key == 'input':
                name = _get_only_name(match.group(key))
                newMod.addName(VerilogName(name, 0))
            elif key == 'inout':
                name = _get_only_name(match.group(key))
                newMod.addName(VerilogName(name, 2))
            elif key == 'output':
                name = _get_only_name(match.group(key))
                newMod.addName(VerilogName(name, 1))
            elif key == 'wire':
                name = _get_only_name(match.group(key))
                newMod.addName(VerilogName(name, 3))

            line = file.readline()
    return modules

def _find_repeated_names(module):
    all_names = module.names

    for idx, name in enumerate(all_names):
        for subname in all_names[idx+1: None]:
            if name.name.lower() == subname.name.lower() and name.name != subname.name:
                # print('______________________ match ______________________', name, subname)
                if name.type == 0 and subname.type == 0:
                    print('______________________ two inputs has the same lowercased name (' + name.name + ' & ' + subname.name + ') ______________________')
                elif name.type == 1 and subname.type == 1:
                    print('______________________ two outputs has the same lowercased name (' + name.name + ' & ' + subname.name + ') ______________________')
                elif name.type == 2 and subname.type == 2:
                    print('______________________ two inouts has the same lowercased name (' + name.name + ' & ' + subname.name + ') ______________________')
                elif name.type == 3 and subname.type == 3:
                    # print('______________________ two wires has the same lowercased name (' + name.name + ' & ' + subname.name + ') ______________________')
                    module.namesToChange.append(subname)
                elif name.type == 3:
                    # print('______________________ need to change name (' + name.name + ') ______________________')
                    module.namesToChange.append(name)
                elif subname.type == 3:
                    # print('______________________ need to change name (' + subname.name + ') ______________________')
                    module.namesToChange.append(subname)


rx_dict = {
    'input'  : re.compile(r'input(?P<input>.*;)'),
    'output' : re.compile(r'output(?P<output>.*;)'),
    'inout'  : re.compile(r'inout(?P<inout>.*;)'),
    'wire'   : re.compile(r'wire(?P<wire>.*;)'),
    'module' : re.compile(r'\bmodule\b(?P<module>.*\w)')
}

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

   modules = []

   filepath = 'tx_handler_bad.phy.v'

   print('Getting key names ...')
   modules = _parse_file(filepath);

   print('Looking for repeated one ...')
   for mod in modules:
       _find_repeated_names(mod)

   print('Modifying modules ...')
   input = open(filepath)
   output = open(filepath+'_fixed', 'w')

   modidx = -1;
   module = VerilogModule('');

   for s in input.readlines():
       new_str = s;

       match = re.compile(r'\bmodule\b', flags=re.I | re.X)
       res = match.search(s)
       if res:
           if res.group() == 'module':
               modidx += 1
               module = modules[modidx]

       if module.name != '':
           for name in module.namesToChange:
               if name.name in s:
                   new_str = re.sub(r'\b'+name.name+r'\b', '/______GENERATED_________'+name.name , new_str)
       output.write(new_str)

   input.close()
   output.close()

if __name__ == '__main__':
    main(sys.argv[1:])
