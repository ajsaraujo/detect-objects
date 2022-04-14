import sys

# Prints error to stdout and then exits with code 1
def error(message):
  print(message)
  exit(1)

# Reads line from the file while ignoring comments
def read_line(file):
  line = file.readline().strip()

  if line[0] == '#':
    return read_line(file)
  
  return line

# Reads a single integer from the next line
def read_int(file):
  return int(read_line(file))

# Creates a matrix filled with zeroes
def zeroes_matrix(height, width):
  return [[0 for column in range(width)] for row in range(height)]

# Reads a pgm file
def read_pgm(file_path):
  file = open(file_path, "r")
  file_type = read_line(file)

  if file_type != 'P1':
    error(f'Expected file type to be P1 (binary), got "{file_type}" instead')

  width, height = map(int, read_line(file).split())
  max_value = read_int(file)

  matrix = zeroes_matrix(height, width)

  for row in range(height):
    for column in range(width):
      matrix[row][column] = read_int(file)

      if matrix[row][column] > max_value:
        found_value = matrix[row][column]
        print(f'Warning: max value is {max_value}, found {found_value} at position ({row}, {column})')
        matrix[row][column] = max_value
  
  return {
    'file_type': file_type,
    'width': width,
    'height': height,
    'max_value': max_value,
    'matrix': matrix
  }

def get_neighbors(i, j):
  deltas = [-1, 0, 1]

  neighbors = []

  for delta_x in deltas:
    for delta_y in deltas:
      neighbor_x = i + delta_x
      neighbor_y = j + delta_y

      if neighbor_x < 0 or neighbor_x >= width:
        continue
      
      if neighbor_y < 0 or neighbor_y >= height:
        continue
      
      neighbors.append([neighbor_x, neighbor_y])
  
  return neighbors

def fill(i, j):
  for neighbor in get_neighbors(i, j):
    m, n = neighbor

    not_visited = tags[m][n] == NO_TAG
    same_color_as_current_pixel = color[i][j] == color[m][n]

    if not_visited and same_color_as_current_pixel:
      fill(m, n)

file_path_was_passed = len(sys.argv) > 1

if not file_path_was_passed:
  error('Please provide an image file path')

file_path = sys.argv[1]
pgm = read_pgm(file_path)
tags = zeroes_matrix(pgm['height'], pgm['width'])
color = pgm['matrix']

NO_TAG = 0
last_tag = 0
height = pgm['height']
width = pgm['width']

for i in range(height):
  for j in range(width):
    if tags[i][j] == NO_TAG:
      last_tag += 1
      fill(i, j)

      if color[i][j] == 0:
        print(f'Found blank space at ({i}, {j})')
      else:
        print(f'Found new object at ({i}, {j}')
      
