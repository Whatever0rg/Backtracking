
class LabrinthMarkers():
    '''
    These are helper variables for the read_labyrinth,
    isFree, and isEscape functions.
    They define the different parameters of the labyrinth.
    '''
    end_point_marker = 'E'
    start_point_marker = 'S'
    border_marker = 'x'


class Moves():
    '''
    These are the moves that pathfinding can perform:
    - north
    - east
    - south
    - west
    There are no diagonal moves.
    '''
    def north(coordinate):
        x, y = coordinate
        y -= 1
        coordinate = x, y
        return coordinate

    def south(coordinate):
        x, y = coordinate
        y += 1
        coordinate = x, y
        return coordinate

    def east(coordinate):
        x, y = coordinate
        x += 1
        coordinate = x, y
        return coordinate

    def west(coordinate):
        x, y = coordinate
        x -= 1
        coordinate = x, y
        return coordinate


def is_free(labrinth, row_number=None,
           collum_number=None, pos=None):
    '''
    The isFree function determines whether the given point
    is the border defined by the LabrinthMarker.border_marker.

    It can take either a tuple (x, y)
    as the position or a row_number (y) and a column_number (x).
    '''

    if pos is not None:
        if labrinth[pos[1]][pos[0]] == LabrinthMarkers.border_marker:
            return False
        else:
            return True
    else:
        if labrinth[row_number][collum_number] == LabrinthMarkers.border_marker:
            return False
        else:
            return True


def is_escape(labrinth, row_number=None,
             collum_number=None, pos=None):
    '''
    The isEscape function determines whether the given point
    is the exit defined by the LabrinthMarker.end_point_marker.

    It can take either a tuple (x, y)
    as the position or a row_number (y) and a column_number (x).
    '''

    if pos is not None:
        if labrinth[pos[1]][pos[0]] == LabrinthMarkers.end_point_marker:
            return True
        else:
            return False
    else:
        if labrinth[row_number][collum_number] == LabrinthMarkers.end_point_marker:
            return True
        else:
            return False


def read_labrinth(filename):
    '''
    This function converts a .txt file
    into a list of lists named labyrinth.

    It will also output the start and end point, if provided.
    If no start point is found, it will be set to (1, 1).
    '''
    with open(filename, 'r') as file:
        stripped_a = file.read().splitlines()
    labrinth = []
    start_point = None
    end_point = None
    for row in range(len(stripped_a)):
        print(labrinth)
        labrinth.append(list(stripped_a[row]))
        for collum in range(len(stripped_a[row])):
            match stripped_a[row][collum]:
                # Man kann einen Startpunkt mit 'S' fest legen
                case LabrinthMarkers.start_point_marker:
                    start_point = (collum, row)
                case LabrinthMarkers.end_point_marker:
                    end_point = (collum, row)

    print(f"x:{len(labrinth[0])} y:{len(labrinth)}")
    if start_point is None:
        start_point = (1, 1)
    return labrinth, start_point, end_point


def add_border(labrinth, start_point, end_point):
    '''
    This function adds a border around
    the given labyrinth to prevent out-of-bounds moves.
    It also moves the start and end points to their new locations.
    '''

    row_width = len(labrinth[0])
    border_labrinth = [[LabrinthMarkers.border_marker for n in range(row_width+2)]]

    for row in range(len(labrinth)):
        border_row = [LabrinthMarkers.border_marker]

        for collum in labrinth[row]:
            border_row.append(collum)
        border_row.append(LabrinthMarkers.border_marker)
        border_labrinth.append(border_row)

    border_labrinth.append([LabrinthMarkers.border_marker for n in range(row_width+2)])
    start_point = Moves.south(Moves.east(start_point))
    end_point = Moves.south(Moves.east(end_point))
    return border_labrinth, start_point, end_point


def print_field(field):
    '''
    This outputs a human readable version of the given list of lists.
    '''
    for row in range(len(field)):
        for collum in range(len(field[row])):
            print(field[row][collum], end="")
        print(end="\n")


def find_escape(field, row_number, column_number, route=()):
    current_point = (row_number, column_number)
    tuple_route = ()
    if route == ():
        route = find_escape_full(field, current_point)
    else:
        new_route = [route]
        route = find_escape_full(field, current_point, route=new_route)
    for i in route:
        tuple_route = tuple_route + (i,)
    return tuple_route


def find_escape_full(labrinth, current_point, end_point=None,
                     route=None, best_route=None, visited=None):
    '''
    This function recursively finds the shortest path between two points.
    To start the search, it requires the labyrinth
    and the start point as input.

    To make the search more efficient,
    it is possible to input an end point as a tuple.
    This will stop the function call isEscape
    and directly compare the current point and the end point.

    The output is a list of tuples representing the moves taken to the exit.
    '''
    if route is None:
        route = []

    if best_route is None:
        best_route = []

    if visited is None:
        visited = {}

    route = route + [current_point]
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
    # Without Tuple, function call isEscape
    if end_point is None:
        if is_escape(labrinth, row_number=current_point[1],
                    collum_number=current_point[0]):
            print(f'Finish reached in {val_moves} moves')
            if val_best >= val_moves or best_route == []:
                print('New best finish')
                best_route = list(route)
            return best_route
    # With Tuple, direct Comparisson
    else:
        if current_point == end_point:
            print(f'Finish reached in {val_moves} moves')

            if val_best >= val_moves or best_route == []:
                print('New best finish')
                best_route = list(route)
            return best_route

    # Possible moves
    for move in (Moves.north, Moves.east, Moves.south, Moves.west):
        next_move = move(current_point)

        if is_free(labrinth, row_number=next_move[1], collum_number=next_move[0]):
            pos_moves.append(next_move)

    # Recursion
    if pos_moves != []:

        for move in pos_moves:
            best_route = find_escape_full(labrinth, move, end_point, route, best_route, visited)

            if best_route:
                result.append((len(best_route), best_route))
        route.pop()

        if result:
            min_best = min(result, key=lambda x: x[0])[1]
            return min_best

    # More pruning obsolete
    else:
        print(f'Hit dead end or moved in a circle')
        return best_route

    return best_route


def print_path(labrinth, route):
    '''
    This function modifies the labyrinth to display 
    the route taken by the path-finding algorithm.
    It then prints a readable version to the terminal. 
    '''
    for i in range(len(route)):
        labrinth[route[i][1]][route[i][0]] = '.'

    print_field(labrinth)


def main():
    # Read in Labrinth
    labrinth, start_point, end_point = read_labrinth("labrinth.txt")
    print_field(labrinth)

    # Add border to Stop outofbounds searching
    labrinth, start_point, end_point = add_border(labrinth, start_point, end_point)
    print_field(labrinth)
    print(f'Start: {start_point}, End: {end_point}')

    # Recursion
    best_route = find_escape(labrinth, start_point[0], start_point[1])
    # Printing solution
    print_path(labrinth, best_route)
    print(f'Start: {start_point}\nEnd: {end_point}\n')
    print(f'Path Lenght: {len(best_route)}')
    print(f'\nFinishing Array:\n{best_route}')


if __name__ == "__main__":
    main()
