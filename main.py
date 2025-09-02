import argparse
import os
import enum
import re


#     ┓         
# ┏┏┓╋┣┓┓┏┏┓┏┓┏┏
# ┗┗┻┗┛┗┛┗┛ ┛┗┫┛
#             ┛ 

# Obfuscation script for Pine Script files
# https://github.com/cathxrsys
# https://t.me/cathxrsys


from myutils import Position, MyType, random_var_name
from replace_spaces import replace_spaces, replace_many_spaces, remove_brackets


parser = argparse.ArgumentParser(description="Obfuscate Pine Script files.")
parser.add_argument("input_path", type=str, help="Path to the PineScript6 file")
args = parser.parse_args()

input_path = args.input_path

version = '//@version=6'

if os.path.isfile(input_path):
    with open(input_path, "r") as file:
        lines = file.readlines()
else:
    print(f"Error: The file {input_path} does not exist.")
    exit(1)

positions = []

for index, line in enumerate(lines):
    if '//@version' in line:
        version = line
    if line.startswith("//"): # убираем комментарии
        continue
    if line.strip() == "": # убираем пустые строки
        continue
    
    line = line.replace('\n', '')

    positions.append(Position(index, line, MyType.line))


def find_vars(code):
    # Одиночные переменные: a = 1, d := 2
    singles = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|:=)', code)
    # В списках: [a, b] = ...
    groups = re.findall(r'\[([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)\]\s*=', code)
    group_vars = [item for group in groups for item in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', group)]
    return set(singles + group_vars)


vars = []

for position in positions:
    position.content = replace_many_spaces(position.content)
    position.content = replace_spaces(position.content)

    vars += find_vars(remove_brackets(position.content))

vars = set(vars)
# rand_names = {v: random_var_name(7) for v in vars}
# for key, value in rand_names.items():
#     for position in positions:
#         position.content = re.sub(rf'(?<!\.)\b{re.escape(key)}\b', value, position.content)
    

# перемешиваем строки















import re
from collections import defaultdict

# def find_vars(code):
#     # Одиночные переменные: a = 1, d := 2
#     singles = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|:=)', code)
#     # В списках: [a, b] = ...
#     groups = re.findall(r'\[([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)\]\s*=', code)
#     group_vars = [item for group in groups for item in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', group)]
#     return set(singles + group_vars)

def find_dependencies(line, all_vars):
    # Находим имя переменной, которая присваивается
    m = re.match(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|:=)', line)
    lhs = m.group(1) if m else None
    
    # Находим все переменные, которые используются в правой части
    rhs = line.split('=', 1)[-1] if '=' in line else line.split(':=', 1)[-1] if ':=' in line else ''
    # Ищем переменные, которые присутствуют в all_vars
    deps = set()
    for var in all_vars:
        # чтобы не ловить подстроки, используем \b
        if re.search(rf'\b{re.escape(var)}\b', rhs) and var != lhs:
            deps.add(var)
    return lhs, deps

def build_dependency_graph(positions):
    # Собираем все переменные
    all_vars = vars
    
    # Строим граф зависимостей
    graph = defaultdict(set)
    for pos in positions:
        lhs, deps = find_dependencies(pos.content, all_vars)
        if lhs:
            graph[lhs].update(deps)
    return graph

# ----- Подробные объяснения -----

# 1. import re и defaultdict: нужны для поиска переменных и хранения графа зависимостей как словаря множеств.
# 2. find_vars: функция для поиска всех объявленных переменных в строке кода.
# 3. find_dependencies: ищет переменную слева от знака = или := (это lhs), затем анализирует правую часть и ищет там все переменные из all_vars (это deps). Используется регулярка с \b чтобы не ловить подстроки.
# 4. build_dependency_graph: проходится по всем строкам, находит все переменные, затем для каждой строки ищет зависимости (lhs, deps) и добавляет в граф.
# 5. Итог: граф - это словарь, где ключ — имя переменной, значение — множество переменных, от которых она зависит.

# ----- Использование -----
# positions — список объектов, например, как у тебя Position(index, content, type)
graph = build_dependency_graph(positions)

# Печать графа
for var, deps in graph.items():
    print(f"{var} зависит от: {', '.join(deps) if deps else 'ничего'}")


# тут нужно мешать










# print('Result:')

# for position in positions:
#     print(position.content)


output_file = input_path.rsplit('.', 1)[0] + '.obfs.' + input_path.rsplit('.', 1)[1]
out = open(output_file, 'w')
out.write(version + '\n')
for position in positions:
    out.write(position.content + '\n')
out.close()

print(f'\nObfuscated file saved as: {output_file}')