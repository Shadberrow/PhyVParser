import re
import sys, getopt
import ntpath

# Definition of type:
#     input = 0 | output = 1 | inout = 2 | wire = 3 | digital = 4

rx_dict = {                                                           # Regular Expression dictionary
    'input'  : re.compile(r'input(?P<input>.*;)'),
    'output' : re.compile(r'output(?P<output>.*;)'),
    'inout'  : re.compile(r'inout(?P<inout>.*;)'),
    'wire'   : re.compile(r'wire(?P<wire>.*;)'),
    'module' : re.compile(r'\bmodule\b(?P<module>.*\w)'),
    'digital': re.compile(r'(?P<digital>\w+)(?=\s\()')
}

class VerilogName:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.strType = "input" if type == 0 else \
            ("output" if type == 1 else
             ("inout" if type == 2 else
              ("wire" if type == 3 else "digital")))

    def __str__(self):
        return "{} {}".format(self.strType, self.name)

    def __repr__(self):
        return "{} {}".format(self.strType, self.name)


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


def _get_key_module_items(line):             # Parse line to find key module components like 'wire', 'input', 'output', and others.
    for key, rx in rx_dict.items():          # Loop through predifined dictionary with searching keys and Regular Expressions
        match = rx.search(line)              # Find any matching
        if match:                            # If line contains information we need (look Regular Expression dictionary)
            return key, match                # Return the information matched Regular Expression
    return None, None                        # If nothing found return None


def _get_design_modules(filepath):
    newMod = VerilogModule('')
    modules = []

    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            key, match = _get_key_module_items(line)

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
            elif key == 'digital':
                name = _get_only_name(match.group(key))
                newMod.addName(VerilogName(name, 4))

            line = file.readline()
    return modules


def _find_repeated_names(module):
    all_names = module.names

    for idx, name in enumerate(all_names):
        for sub_name in all_names[idx + 1: None]:
            if name.name.lower() == sub_name.name.lower() and name.name != sub_name.name:
                if name.type == 0 and sub_name.type == 0:
                    print('**! Two inputs has the same name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 1 and sub_name.type == 1:
                    print('**! Two outputs has the same name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 2 and sub_name.type == 2:
                    print('**! Two inouts has the same name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 3 and sub_name.type == 3:
                    print('**! Two wires has the same name (' + name.name + ' & ' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)
                elif name.type == 4 and sub_name.type == 4:
                    print('**! Two digital components has the same name (' + name.name + ' & ' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)
                elif name.type == 3:
                    print('**! Need to change wire name (' + name.name + ')')
                    module.namesToChange.append(name)
                elif sub_name.type == 3:
                    print('**! Need to change wire name (' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)


def _edit_and_save(filepath, modules):
    head, tail = ntpath.split(filepath)
    if head: head = head + '/'
    outputFilepath = head + 'FIXED_' + tail
    input = open(filepath)
    output = open(outputFilepath, 'w')

    modidx = -1
    module = VerilogModule('')

    for string in input.readlines():
        new_str = string

        match = re.compile(r'\bmodule\b', flags=re.I | re.X)
        res = match.search(string)
        if res and res.group() == 'module':
            modidx += 1
            module = modules[modidx]

        if module.name != '':
            for name in module.namesToChange:
                if name.name in string:
                    new_str = re.sub(r'\b' + name.name + r'\b', 'FCNN_' + name.name, new_str)
        output.write(new_str)

    input.close()
    output.close()
    print('Result saved in ' + outputFilepath)


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('netreplace.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('netreplace.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            if inputfile == '':
                print('netreplace.py -i <inputfile>')
                sys.exit()

    file_path = inputfile

    print('Getting key names ...')
    modules = _get_design_modules(file_path)

    print('Looking for duplicates ...')
    hasRepeatedItems = False
    for mod in modules:
        _find_repeated_names(mod)
        if len(mod.namesToChange) > 0:
            try:
                print("\n\nFOUND REPEATED NAMES IN MODULE: {m.name}\n\n {m.namesToChange}".format(m=mod))
            except:
                print("\n\nFOUND REPEATED NAMES IN MODULE: {m.name} - {len(m.namesToChange)}\n\n".format(m=mod))
            print("\nPROCESSING ...\n")
            hasRepeatedItems = True

    if hasRepeatedItems:
        print('Modifying modules ...')
        _edit_and_save(file_path, modules)
    else:
        print('File doesnt have repeated net names.')
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('netreplace.py -i <inputfile>')
        sys.exit()
    else:
        main(sys.argv[1:])
