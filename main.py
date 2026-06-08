from operator import itemgetter
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
        stripped_a=file.read().splitlines()
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



def backtrack(labrinth,current_point,end_point,moves_ary=None,best=None,visited=None):
    #print("ENTER", current_point, moves_ary) # For debugging purposes
    if moves_ary is None:
        moves_ary=[]
    
    if best is None:
        best=[]
    
    if visited is None:
        visited = {}

    moves_ary= moves_ary+[current_point]
    val_moves=len(moves_ary)
    val_best=len(best)
    pos_moves=[]
    result=[]

    # Early branch pruning
    if best and val_moves >= val_best:
        return best

    if current_point in visited and visited[current_point] <= val_moves:
        moves_ary.pop()
        return best
    else:
        visited[current_point] = val_moves

    # Win condition
    if current_point == end_point:
        print(f'Finish reached in {val_moves} moves')

        if val_best >= val_moves or best == []:
            print('New best finish')
            best = list(moves_ary)
        return best
    
    # Possible moves
    for move in (Moves.N,Moves.O,Moves.S,Moves.W):
        next_move = move(current_point)

        if not isBarrier(labrinth,next_move):
            pos_moves.append(next_move)
                        
    # Recursion
    if pos_moves != []:

        for move in pos_moves:
            best = backtrack(labrinth,move,end_point,moves_ary,best,visited)
            #print("TRY", current_point, "->", move) # For debugging puposes
            if best:
                result.append((len(best),best))
        moves_ary.pop()

        if result:
            min_best = min(result, key=lambda x:x[0])[1]
            return min_best
    
    # More pruning
    else:
        print(f'Hit dead end or moved in a circle')
        return best

    return best
    
        
        


def print_path(labrinth,moves_ary):
    for i in range(len(moves_ary)):
        labrinth[moves_ary[i][1]][moves_ary[i][0]]='.'
    print_field(labrinth)
        


def main():
    labrinth, start_point, end_point = read_labrinth("labrinth.txt")
    print_field(labrinth)
    labrinth, start_point, end_point=add_border(labrinth,start_point,end_point)
    print_field(labrinth)
    print(f'Start: {start_point}, End: {end_point}')
    best = backtrack(labrinth,start_point,end_point)
    print_path(labrinth,best)
    print(f'Start: {start_point}\nEnd: {end_point}\nPath Lenght: {len(best)}\nFinishing Array:\n{best}')



if __name__ == "__main__":
    main()