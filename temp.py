def startswithword(line: str) -> bool:
    f = False
    for i, c in enumerate(line):
        if (c.isalnum() and not c.isnumeric()) or (c == '_' and i != 0):
            f = True
        elif c == ' ' and f:
            return True
        else:
            return False
    return False
        

assert startswithword('var label stoch_label = na') == True
assert startswithword('var!') == False
assert startswithword('rld!!!" ;') == False


def replace_spaces(line: str) -> str:
    f = False
    quote = False
    w = False

    with open('dict.txt', 'r') as wordfile:
        words = wordfile.read().splitlines()

    result = ""
    for i, c in enumerate(line):
        s = line[i-1:] if i > 0 else ''

        for word in words:
            if startswithword(s):
                # print(s)
                w = True

        if w and c == ' ':
            w = False
            result += c
        elif w and c != ' ':
            result += c
            continue

        if c == '"':
            quote = not quote
            f = False
        if c == ' ' and not f:
            result += c
        elif c == ' ' and quote:
            result += c
        elif c == ' ' and f:
            continue
        else:
            result += c
            f = True

    replaces_map = {
        ' = ' : '=',
        ' =' : '=',
        '= ' : '=',
    }

    for old, new in replaces_map.items():
        result = result.replace(old, new)

    return result



assert replace_spaces('    123 562 223') == '    123562223'
assert replace_spaces('123 562 223') == '123562223'
assert replace_spaces('    123 562 223    ') == '    123562223'
assert replace_spaces('    list l[1, 3] = "hello, world!!!" ;   ') == '    list l[1,3]="hello, world!!!";'
assert replace_spaces('var label stoch_label = na') == 'var label stoch_label=na'
assert replace_spaces('if showOscMap and barstate.islast') == 'if showOscMap and barstate.islast'
assert replace_spaces('') == ''
assert replace_spaces('') == ''



# var label stoch_label = na
# if showOscMap and barstate.islast

print('test passed successfully')