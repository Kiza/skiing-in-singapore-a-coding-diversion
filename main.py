# run with python 3.5.1

MAX_ELEVATION = 1501
MIN_LENGTH = 0

def load_map(mapfile):
    line_num = 0
    dimension = []
    mapdata = []
    with open(mapfile, 'r') as f:
        for line in f:
            line_num = line_num + 1
            if line_num == 1:
                dimension = [ int(i) for i in line.strip().split(' ')]
            else:
                mapdata.append([ int(i) for i in line.strip().split(' ')])

    return (dimension, mapdata)

def print_map(dimension, mapdata):
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            print(str(mapdata[i][j]) + " ", end="")
        print()

def compare_path(a, b):
    # for a fix starting point,
    # we are looking for
    # 1. longest length
    # 2. lowest ending points

    a_length = a[0]
    a_elevation = a[1]
    b_length = b[0]
    b_elevation = b[1]
    if a_length > b_length:
        return (a_length, a_elevation)

    if b_length > a_length:
        return (b_length, b_elevation)

    if a_length == b_length:
        if a_elevation < b_elevation:
            return (a_length, a_elevation)

        if b_elevation < a_elevation:
            return (b_length, b_elevation)

    return (a_length, a_elevation)


def longest_path_from(x, y, dimension, mapdata, records):
    if records[x][y] is not None:
        return records[x][y]

    (max_length, min_elevation) = (MIN_LENGTH, MAX_ELEVATION)
    path_found = False

    # check right,
    if y+1 < dimension[1] and mapdata[x][y] > mapdata[x][y+1]:
        path_found = True
        (_length, _elevation) = longest_path_from(x, y+1, dimension, mapdata, records)
        (max_length, min_elevation) = compare_path((max_length, min_elevation), (_length, _elevation))


    # check left,
    if y-1 >= 0 and mapdata[x][y] > mapdata[x][y-1]:
        path_found = True
        (_length, _elevation) = longest_path_from(x, y-1, dimension, mapdata, records)
        (max_length, min_elevation) = compare_path((max_length, min_elevation), (_length, _elevation))

    # check up,
    if x-1 >= 0 and mapdata[x][y] > mapdata[x-1][y]:
        path_found = True
        (_length, _elevation) = longest_path_from(x-1, y, dimension, mapdata, records)
        (max_length, min_elevation) = compare_path((max_length, min_elevation), (_length, _elevation))

    # check down,
    if x+1 < dimension[0] and mapdata[x][y] > mapdata[x+1][y]:
        path_found = True
        (_length, _elevation) = longest_path_from(x+1, y, dimension, mapdata, records)
        (max_length, min_elevation) = compare_path((max_length, min_elevation), (_length, _elevation))

    if path_found:
        # found a path,
        (max_length, min_elevation) = (max_length + 1, min_elevation)
    else:
        # if no where to go
        # set distance to 1
        # set the lowest point to its own altitude
        (max_length, min_elevation) = (1, mapdata[x][y])

    records[x][y] = (max_length, min_elevation)
    return (max_length, min_elevation)


def find_longest_path(dimension, mapdata):
    records = [ [None for i in range(dimension[1])] for j in range(dimension[0]) ]

    for i in range(dimension[0]):
        for j in range(dimension[1]):
            if records[i][j] is None:
                longest_path_from(i, j, dimension, mapdata, records)

    result = {}
    result['length']  = MIN_LENGTH
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            _length = records[i][j][0]
            if _length > result['length']:
                result['length'] = _length
                _elevation = mapdata[i][j]
                _min_elevation = records[i][j][1]
                result['drop'] = _elevation - _min_elevation
            elif _length == result['length']:
                _drop = mapdata[i][j] - records[i][j][1]
                if _drop > result['drop']:
                    result['length'] = _length
                    _elevation = mapdata[i][j]
                    _min_elevation = records[i][j][1]
                    result['drop'] = _elevation - _min_elevation

    print(result)
    print("Email: {0}{1}@redmart.com".format(result['length'], result['drop']))



def main():
    print('Reading map data ...')
    (dimension, mapdata) = load_map("map.txt")
    print('Done reading map data.')
    print('Map dimension: {0}'.format(str(dimension)))
    find_longest_path(dimension, mapdata)



if __name__ == "__main__":
    main()
