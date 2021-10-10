import inspect

def get_used_coordinates(board):
    used_coordinates = []

    for x in range(7):
        for y in range(7):
            if len(board[y][x]) != 0:
                used_coordinates.append((y, x))

    return used_coordinates

'''
simple_board = {}
def create_simple_board(board):
    used_coordinates = get_used_coordinate_values(board)

    for coordinate in used_coordinates:
        simple_board[coordinate] = 
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

board = [[[] for _ in range(7)] for _ in range(7)]

board[0][0].append(dax)
board[6][3].append(bill)
simple_board = {}

for coordinate in get_used_coordinates(board):
    simple_board[coordinate] = []

    for obj in board[coordinate[1]][coordinate[0]]:
        simple_board[coordinate].append(obj.__dict__)

print(simple_board, '\n')
