import enum
import random
import string


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


def random_var_name(length: int = 8) -> str:
    if length < 5:
        raise ValueError("Length must be at least 1")

    first_char = random.choice(['C','X','T'])
    second_char = random.choice(['H','R','S'])
    third_char = random.choice(['Y'])
    other_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 4))
    return first_char + second_char + third_char + first_char + other_chars