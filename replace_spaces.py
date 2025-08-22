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


def replace_spaces(line: str) -> str:
    f = False
    quote = False
    w = False
    n = False

    with open('dict.txt', 'r') as wordfile:
        words = wordfile.read().splitlines()

    result = ""
    for i, c in enumerate(line):
        s = line[i-1:] if i > 0 else ''

        # for word in words:
        if startswithword(s):
                # print(s)
            w = True

        if n and c == ' ':
            result += c
            continue

        if c.isnumeric():
            n = True
        else:
            n = False

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
        '< ' : '<',
        ' <' : '<',
        ' < ' : '<',
        ' >' : '>',
        '> ' : '>',
        ' > ': '>',
        '? ' : '?',
        ' ?' : '?',
        ' ? ' : '?',
        '* ' : '*',
        ' *' : '*',
        ' * ' : '*',
        ' +' : '+',
        '+ ' : '+',
        ' + ' : '+',
        ': ' : ':',
        ' :' : ':',
        ' : ' : ':',
        ' -' : '-',
        '- ' : '-',
        ' - ' : '-',
        '/ ' : '/',
        ' /' : '/',
        ' / ' : '/',
        ' !=' : '!=',
        '!= ' : '!=',
        ' != ' : '!=',
    }

    for old, new in replaces_map.items():
        result = result.replace(old, new)

    return result


def replace_many_spaces(line: str) -> str:
    f = True
    j = 0
    q = False
    result = ''
    for i, c in enumerate(line):
        if c == '"': q = not q
        if f and c == ' ' or q:
            result += c
            continue
        elif f and c != ' ':
            f = False
            j = 0
            result += c
        elif not f and c == ' ':
            j += 1
            if j <= 1:
                result += c
        else:
            result += c
            j = 0
    return result


def remove_brackets(line: str) -> str:
    b = 0
    result = ''
    for i, c in enumerate(line):
        if c == '(':
            b += 1
            continue
        elif c == ')':
            b -= 1
            continue
        if b == 0:
            result += c
    return result


replace_spaces('if CSYCQWT>=-70 and CSYCQWT<=-30')

if __name__ == '__main__':
    assert remove_brackets('func(a, b) + (c + d)') == 'func + '
    print('.', end='')
    assert remove_brackets('((a + b) * (c - d)) / e') == ' / e'
    print('.', end='')
    assert remove_brackets('no brackets here') == 'no brackets here'
    print('.', end='')
    assert remove_brackets('(a + (b * c) - d) / e') == ' / e'
    print('.', end='')
    assert remove_brackets('((()))') == ''
    print('.', end='')
    print('\ntests "remove_brackets" passed successfully')

    assert replace_many_spaces('    var label      stoch_label    =      na') == '    var label stoch_label = na'
    assert replace_many_spaces('    var label      stoch_label    =      "Hello   World!!!   "   var') == '    var label stoch_label = "Hello   World!!!   " var'
    print('.', end='')

    print('\ntests "replace_many_spaces" passed successfully')


    assert startswithword('var label stoch_label = na') == True
    print('.', end='')
    assert startswithword('var!') == False
    print('.', end='')
    assert startswithword('rld!!!" ;') == False
    print('.', end='')

    print('\ntests "startswithword" passed successfully')

    
    assert replace_spaces('if CSYCQWT>=-70 and CSYCQWT<=-30') == 'if CSYCQWT>=-70 and CSYCQWT<=-30'
    print('.', end='')
    assert replace_spaces('    list l[1, 3] = "hello, world!!!" ;   ') == '    list l[1,3]="hello, world!!!";'
    print('.', end='')
    assert replace_spaces('var label stoch_label = na') == 'var label stoch_label=na'
    print('.', end='')
    assert replace_spaces('if showOscMap and barstate.islast') == 'if showOscMap and barstate.islast'
    print('.', end='')
    assert replace_spaces('') == ''
    print('.', end='')
    assert replace_spaces('') == ''
    print('.', end='')

    print('\ntests "replace_spaces" passed successfully')