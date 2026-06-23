

class LabrintheMarkers():
    '''
    These are helper Varibles for the read_labrinth , isFree and isEscape function.
    It defines the diffrent Parameters of the labrinth.
    '''
    end_point_marker = 'E'
    start_point_marker = 'S'
    border_marker = 'x'


class Moves():
    '''
    These are the Moves the Path finding can do:
    - north
    - east
    - south
    - west
    there are no diaglnal moves.
    '''
    def north(coordinate):
        x,y = coordinate
        y -=1
        coordinate = x,y
        return coordinate

    def south(coordinate):
        x,y = coordinate
        y +=1
        coordinate = x,y
        return coordinate

    def east(coordinate):
        x,y = coordinate
        x +=1
        coordinate = x,y
        return coordinate

    def west(coordinate):
        x,y = coordinate
        x -=1
        coordinate = x,y
        return coordinate


def isFree(labrinth,row_number=None,
           collum_number=None,pos=None): 
    '''
    The isFree function checks if the given point is a Border as 
    defined by LabrinthMarker.border_marker.

    It can either take a tuple (x,y) as pos,
    or it can take row_number = y and collum_number = x.
    '''
    if pos is not None:
        if labrinth[pos[1]][pos[0]] == LabrintheMarkers.border_marker:
            return False
        else:
            return True
    else:
        if labrinth[row_number][collum_number] == LabrintheMarkers.border_marker:
            return False
        else:
            return True
    
def isEscape(labrinth,row_number=None,
             collum_number=None,pos=None):
    '''
    The isEscape function checks if the given point is the Exit as 
    defined by LabrinthMarker.end_point_marker.

    It can either take a tuple (x,y) as pos,
    or it can take row_number = y and collum_number = x.
    '''
    if pos is not None:
        if labrinth[pos[1]][pos[0]] == LabrintheMarkers.end_point_marker:
            return True
        else:
            return False
    else:
        if labrinth[row_number][collum_number] == LabrintheMarkers.end_point_marker:
            return True
        else:
            return False


def read_labrinth(filename):
    '''
    This function will convert a .txt file to a list of lits named labrinth.

    It also outputs the start and end_point if given.
    If no start point is found it will be set to (1,1).
    '''
    with open(filename,'r') as file:
        stripped_a = file.read().splitlines()
    labrinth = []
    start_point = None
    end_point = None
    for row in range(len(stripped_a)):
        print(labrinth)
        labrinth.append(list(stripped_a[row]))
        for collum in range(len(stripped_a[row])):
            match stripped_a[row][collum]:
                case LabrintheMarkers.start_point_marker: # Mit 'S' im laberinth 
                    start_point = (collum,row)
                case LabrintheMarkers.end_point_marker:
                    end_point = (collum,row)

    print(f"x:{len(labrinth[0])} y:{len(labrinth)}")
    if start_point == None:
        start_point = (1,1)
    return labrinth, start_point, end_point


def add_border(labrinth,start_point,end_point):
    '''
    This function will add a border around the given labrinth to prevent outofbounds moves.
    It also moves the start and end_point to their new locations.
    '''
    row_width = len(labrinth[0])
    border_labrinth=[[LabrintheMarkers.border_marker for n in range(row_width+2)]]

    for row in range(len(labrinth)):
        border_row=[LabrintheMarkers.border_marker]

        for collum in labrinth[row]:
            border_row.append(collum)
        border_row.append(LabrintheMarkers.border_marker)
        border_labrinth.append(border_row)

    border_labrinth.append([LabrintheMarkers.border_marker for n in range(row_width+2)])
    start_point = Moves.south(Moves.east(start_point))
    end_point = Moves.south(Moves.east(end_point))
    return border_labrinth,start_point,end_point


def print_field(field):
    '''
    This outputs a human readable version of the given list of lists.
    '''
    for row in range(len(field)):
        for collum in range(len(field[row])):
            print(field[row][collum],end="")
        print(end="\n")


def find_escape(labrinth,current_point,end_point=None,
                route=None,best_route=None,visited=None):
    '''
    This function recursively finds the shortest path between two points.
    It needs the labrinth and the start_point as input to start the search.

    To make the search more efficient, it is possible to input a tuple end_point.
    This will stop the function call isEscape and just directly compare current_point and end_point

    The Output is list of tuples which represent the moves taken to the exit.
    '''
    if route is None:
        route=[]
    
    if best_route is None:
        best_route=[]
    
    if visited is None:
        visited = {}

    route = route+[current_point]
    val_moves = len(route)
    val_best = len(best_route)
    pos_moves = []
    result = []

    # Early branch pruning
    if best_route and val_moves >= val_best:
        return best_route

    if current_point in visited and visited[current_point] <= val_moves:
        route.pop()
        return best_route
    else:
        visited[current_point] = val_moves

    # Win condition
    # Ohne Tuple, function call isEscape
    if end_point is None: 
        if isEscape(labrinth,row_number=current_point[1],
                    collum_number=current_point[0]):
            print(f'Finish reached in {val_moves} moves')
            if val_best >= val_moves or best_route == []:
                print('New best finish')
                best_route = list(route)
            return best_route
    # Mit Tuple, direkter Vergleich  
    else:
        if current_point == end_point:
            print(f'Finish reached in {val_moves} moves')

            if val_best >= val_moves or best_route == []:
                print('New best finish')
                best_route = list(route)
            return best_route
    
    # Possible moves
    for move in (Moves.north,Moves.east,Moves.south,Moves.west):
        next_move = move(current_point)

        if isFree(labrinth,row_number=next_move[1],collum_number=next_move[0]):
            pos_moves.append(next_move)
                        
    # Recursion
    if pos_moves != []:

        for move in pos_moves:
            best_route = find_escape(labrinth,move,end_point,route,best_route,visited)

            if best_route:
                result.append((len(best_route),best_route))
        route.pop()

        if result:
            min_best = min(result, key=lambda x:x[0])[1]
            return min_best
    
    # More pruning obsolete
    else:
        print(f'Hit dead end or moved in a circle')
        return best_route

    return best_route


def print_path(labrinth,route):
    '''
    This function modifies the labrinth to show the route taken by the path finding algo.
    It then prints a humanredable version to the Terminal.
    '''
    for i in range(len(route)):
        labrinth[route[i][1]][route[i][0]] = '.'

    print_field(labrinth)
        

def main():
    # Read in Labrinth
    labrinth, start_point, end_point = read_labrinth("labrinth.txt")
    print_field(labrinth)

    # Add border to Stop outofbounds searching
    labrinth, start_point, end_point = add_border(labrinth,start_point,end_point)
    print_field(labrinth)
    print(f'Start: {start_point}, End: {end_point}')

    # Recursion
    # hier könnte man eine Variable names end_point = (x,y)
    # über geben um die isEscape abfrage einzusparen.
    best_route = find_escape(labrinth,start_point) 

    # Printing solution
    print_path(labrinth,best_route)
    print(f'Start: {start_point}\nEnd: {end_point}\nPath Lenght: {len(best_route)}\nFinishing Array:\n{best_route}')


if __name__ == "__main__":
    main()
