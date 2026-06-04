from operator import itemgetter
from numpy import copy
from time import sleep



class LabrintheMarkers():
    end_point_marker = 'z'
    start_point_marker = 's'
    border_marker = 'x'

class Moves():
    def N(coordinate):
        x,y = coordinate
        y -=1
        coordinate = x,y
        return coordinate

    def S(coordinate):
        x,y = coordinate
        y +=1
        coordinate = x,y
        return coordinate

    def O(coordinate):
        x,y = coordinate
        x +=1
        coordinate = x,y
        return coordinate

    def W(coordinate):
        x,y = coordinate
        x -=1
        coordinate = x,y
        return coordinate
    
    def cost(start,position,end):
        s_cost= abs(position[0]-start[0])+abs(position[1]-start[1])
        f_cost= abs(position[0]-end[0])+abs(position[1]-end[1])
        result= s_cost + f_cost
        return result, s_cost, f_cost

def isBarrier(labrinth,pos):
    if labrinth[pos[1]][pos[0]] == 'x':
        return True
    else:
        return False

def read_labrinth(filename):
    with open(filename,'r') as file:
        a=list(file)
        stripped_a =[row.strip() for row in a]
    labrinth=[]
    for row in range(len(stripped_a)):
        print(labrinth)
        labrinth.append(list(stripped_a[row]))
        for collum in range(len(stripped_a[row])):
            match stripped_a[row][collum]:
                case LabrintheMarkers.start_point_marker:
                    start_point = (collum,row)
                case LabrintheMarkers.end_point_marker:
                    end_point = (collum,row)

    print(f"x:{len(labrinth[0])} y:{len(labrinth)}")
    return labrinth, start_point, end_point

def add_border(labrinth,start_point,end_point):
    row_width = len(labrinth[0])
    border_labrinth=[['x' for n in range(row_width+2)]]
    for row in range(len(labrinth)):
        border_row=['x']
        for collum in labrinth[row]:
            border_row.append(collum)
        border_row.append('x')
        border_labrinth.append(border_row)
    border_labrinth.append(['x' for n in range(row_width+2)])
    start_point=Moves.S(Moves.O(start_point))
    end_point=Moves.S(Moves.O(end_point))
    return border_labrinth,start_point,end_point

def print_field(field):
    for row in range(len(field)):
        for collum in range(len(field[row])):
            print(field[row][collum],end="")
        print(end="\n")



def backtrack(labrinth,start_point,last_move,end_point,moves_ary=[],k_path=None):
    canMove = False
    moves_ary.append(last_move)
    if last_move==end_point:
        print("Finish reached")
        if k_path is None or len(moves_ary) <= k_path:
            k_path=len(moves_ary)
        return (len(moves_ary), moves_ary),k_path
    

    possible_moves = []
    for move in [Moves.N,Moves.S,Moves.O,Moves.W]:
        next_pos = move(last_move)
        if not isBarrier(labrinth,next_pos):
            possible_moves.append((move,Moves.cost(start_point,next_pos,end_point)))
    res_moves = sorted(possible_moves,key=itemgetter(1))
    path = []
    
    for move, val in res_moves:
        next_pos = move(last_move)
        if next_pos not in moves_ary:
            if k_path is None or len(moves_ary) <= k_path:
                print(val)
                result, k_path = backtrack(
                    labrinth,
                    start_point,
                    next_pos,
                    end_point,
                    moves_ary.copy(),
                    k_path
                )

                if result is not None:
                    path.append(result)

    if path:
        return min(path, key=lambda p: p[0])

    return None

def print_path(labrinth,moves_ary):
    for i in range(len(moves_ary)):
        labrinth[moves_ary[i][1]][moves_ary[i][0]]='.'
        print_field(labrinth)


def main():
    labrinth, start_point, end_point = read_labrinth("labrinth.txt")
    print_field(labrinth)
    labrinth, start_point, end_point=add_border(labrinth,start_point,end_point)
    print_field(labrinth)
    print(start_point, end_point)
    length, move_ary = backtrack(labrinth,start_point,start_point, end_point)
    print_path(labrinth,move_ary)
    print(f'Start: {start_point}\nEnd: {end_point}\nPath Lenght: {length}\nFinishing Array:\n{move_ary}')



if __name__ == "__main__":
    main()