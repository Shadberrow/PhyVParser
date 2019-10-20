import re
import collections
import fileinput
import random
import string
import os, sys

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def _parse_file(filepath):
    data = []
    with open(filepath, 'r') as file:
        line = file.readline()
        while line:
            key, match = _parse_line(line)

            if key == 'input':
                input = match.group('input')
                data.append(input)
            if key == 'inout':
                input = match.group('inout')
                data.append(input)
            if key == 'output':
                input = match.group('output')
                data.append(input)
            if key == 'wire':
                input = match.group('wire')
                data.append(input)

            line = file.readline()

    return data

rx_dict = {
    'input': re.compile(r'input(?P<input>.*);'),
    'output': re.compile(r'output(?P<output>.*);'),
    'inout': re.compile(r'inout(?P<inout>.*);'),
    'wire': re.compile(r'wire(?P<wire>.*);')
}

if __name__ == '__main__':
    filepath = 'sample01.v'
    data = _parse_file(filepath)
    # print(data)

    data = map(lambda x: x.lower(), data)
    data = map(lambda x: x.strip(), data)

    repeated = [item for item, count in collections.Counter(data).items() if count > 1]
    print(repeated)
