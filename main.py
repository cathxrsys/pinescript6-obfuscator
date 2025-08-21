import argparse
import os
import enum


#     ┓         
# ┏┏┓╋┣┓┓┏┏┓┏┓┏┏
# ┗┗┻┗┛┗┛┗┛ ┛┗┫┛
#             ┛ 

# Obfuscation script for Pine Script files
# https://github.com/cathxrsys
# https://t.me/cathxrsys


parser = argparse.ArgumentParser(description="Obfuscate Pine Script files.")
parser.add_argument("input_path", type=str, help="Path to the PineScript6 file")
args = parser.parse_args()

input_path = args.input_path


class MyType(enum.StrEnum):
    integer = '0'
    variable = 'v'
    function = 'f'
    other = '_'
    line = 'l'


class Position:
    def __init__(self, index: int, content: str, type: MyType):
        self._index = index
        self._content = content
        self._type = type

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Index must be an integer.")
        self._index = value
    
    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Content must be a string.")
        self._content = value
    
    @property
    def type(self) -> MyType:
        return self._type

    @type.setter
    def type(self, value: MyType):
        if not isinstance(value, MyType):
            raise TypeError("Type must be an instance of MyType enum.")
        self._type = value

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self._index == other._index

    def __lt__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self._index < other._index

    def __gt__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self._index > other._index


if os.path.isfile(input_path):
    with open(input_path, "r") as file:
        lines = file.readlines()
else:
    print(f"Error: The file {input_path} does not exist.")
    exit(1)

positions = []

for index, line in enumerate(lines):
    if line.startswith("//"): # убираем комментарии
        continue
    if line.strip() == "": # убираем пустые строки
        continue
    
    line = replace_spaces(line)

    positions.append(Position(index, line.strip(), MyType.line))


for position in positions:
    print(position.index, position.content, position.type)