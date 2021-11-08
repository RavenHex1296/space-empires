import inspect
import math, random

'''
class Student():
    def __init__(self, age, grade, name):
        self.age = age
        self.grade = grade
        self.name = name

dax = Student(14, 9, 'Dax li')
bill = Student(12, 7, 'Bill Dipperly')
print(list(dax.__dict__.keys()), '\n')
print(dax.__dict__, '\n')

board = {}

board[0][0].append(dax)
board[6][3].append(bill)
simple_board = {}

for coordinate in get_used_coordinates(board):
    simple_board[coordinate] = []

    for obj in board[coordinate[1]][coordinate[0]]:
        simple_board[coordinate].append(obj.__dict__)

print(simple_board, '\n')
'''

#if roll(1, 10) < atk.atk - df.df
#scout_atk = 3 , scout_ hp = 1, scout_df = 0
#bc atk = 5, bc hp = 2, bc df = 1
data = {'hit': 0, 'miss': 0}
n = 100000

for _ in range(n):
    if random.randint(1, 10) <= 5:
        data['hit'] += 1

    else:
        data['miss'] += 1

print("Bc attacking scout", data, data['hit'] / (data['hit'] + data['miss']))

data = {'hit': 0, 'miss': 0}

for _ in range (n):
    if random.randint(1, 10) <= 4:
        data['hit'] += 1

    else:
        data['miss'] += 1

print("Bc attacking bc", data, data['hit'] / (data['hit'] + data['miss']))


data = {'hit': 0, 'miss': 0}

for _ in range (n):
    if random.randint(1, 10) <= 2:
        data['hit'] += 1

    else:
        data['miss'] += 1

print("scout attacking bc", data, data['hit'] / (data['hit'] + data['miss']))


data = {'hit': 0, 'miss': 0}

for _ in range (n):
    if random.randint(1, 10) <= 3:
        data['hit'] += 1

    else:
        data['miss'] += 1

print("scout attacking scout", data, data['hit'] / (data['hit'] + data['miss']))
