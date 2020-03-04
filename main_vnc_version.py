import re
import sys, getopt


# Definition of type:
#     input = 0 | output = 1 | inout = 2 | wire = 3 | digital = 4

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


def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def _parse_file(filepath):
    newMod = VerilogModule('')
    modules = []

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
                # print('______________________ match ______________________', name, sub_name)
                if name.type == 0 and sub_name.type == 0:
                    print('**! Two inputs has the same lowercase name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 1 and sub_name.type == 1:
                    print('**! Two outputs has the same lowercase name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 2 and sub_name.type == 2:
                    print('**! Two inouts has the same lowercase name (' + name.name + ' & ' + sub_name.name + ')')
                elif name.type == 3 and sub_name.type == 3:
                    print('**! Two wires has the same lowercase name (' + name.name + ' & ' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)
                elif name.type == 4 and sub_name.type == 4:
                    print('**! Two digitals has the same lowercase name (' + name.name + ' & ' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)
                elif name.type == 3:
                    print('**! Need to change name (' + name.name + ')')
                    module.namesToChange.append(name)
                elif sub_name.type == 3:
                    print('**! Need to change name (' + sub_name.name + ')')
                    module.namesToChange.append(sub_name)


def _edit_and_save(filepath, modules):
    outputFilepath = 'FIXED_' + filepath
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


rx_dict = {
    'input': re.compile(r'input(?P<input>.*;)'),
    'output': re.compile(r'output(?P<output>.*;)'),
    'inout': re.compile(r'inout(?P<inout>.*;)'),
    'wire': re.compile(r'wire(?P<wire>.*;)'),
    'module': re.compile(r'\bmodule\b(?P<module>.*\w)'),
    'digital': re.compile(r'(?P<digital>\w+)(?=\s\()')
}


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            if inputfile == '':
                print('test.py -i <inputfile>')
                sys.exit()

    file_path = inputfile

    print('Getting key names ...')
    modules = _parse_file(file_path)

    print('Looking for repeated one ...')
    hasRepeatedItems = False
    for mod in modules:
        _find_repeated_names(mod)
        if len(mod.namesToChange) > 0:
            print("\n\nHAVE FOUNDED REPEATED NAMES IN MODULE: {}\n\n{}\n\nPROCESSING ...\n".format(mod.name, mod.namesToChange))
            hasRepeatedItems = True

    if hasRepeatedItems:
        print('Modifying modules ...')
        _edit_and_save(file_path, modules)
    else:
        print('File doesnt have repeated net names.')
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('test.py -i <inputfile>')
        sys.exit()
    else:
        main(sys.argv[1:])
