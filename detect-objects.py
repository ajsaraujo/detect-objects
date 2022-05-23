import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

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

  matrix = zeroes_matrix(height, width)

  for row in range(height):
    new_line = read_line(file).split()
    for column in range(width):
      matrix[row][column] = int(new_line[column])
  
  return {
    'file_type': file_type,
    'width': width,
    'height': height,
    'matrix': matrix
  }

# Find the seed element to fill the holes in the image
def find_seed(M, N, f):
    for x in range(M):
        for y in range(N):
            if f[x][y] == 1:
                return x, y

# Invert pixels values 0 and 1
def invert_image(M, N, f):
    g = [[0]*(N) for i in range(M)]
    for x in range(M):
        for y in range(N):
            if f[x][y] == 1:
                g[x][y] = 0
            else:
                g[x][y] = 1

    return g

# Dilates an image using a cross as a structuring element
def dilatation_cross(M, N, g):
  h = [[0]*(N) for i in range(M)]
  for x in range(M):
    for y in range(N):
        for neighbor in get_neighbors_4(x, y):
          m, n = neighbor
          if m <= M-1 and n <= N-1 and g[m][n] == 1:
            h[x][y] = 1
            break
    
  return h

# Apply AND logical operator between the pixels of two images
def and_operator(M, N, f, g):
    h = [[0]*(N) for i in range(M)]
    for x in range(M):
        for y in range(N):
            h[x][y] = g[x][y] and f[x][y]
    return h

# Check if matrix are equals
def is_matrix_equals(M, N, f, g):
    for x in range(M):
        for y in range(N):
            if f[x][y] != g[x][y]:
                return False
    return True

# Fill holes in a image
def fill_holes(M, N, f):
    i, j = find_seed(M, N, f)
    g = [[0]*(N) for i in range(M)]
    g[i][j] = 1
    inverted_f = invert_image(M, N, f)
    g_next = and_operator(M, N, dilatation_cross(M, N, g), inverted_f)

    while(is_matrix_equals(M, N, g, g_next) == False):
        g = g_next
        g_next = and_operator(M, N, dilatation_cross(M, N, g), inverted_f)

    g_next = invert_image(M, N,g_next)

    return g_next

# Get 4 neighbors horizontal and vertical of a pixel
def get_neighbors_4(i, j):
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
      
      if neighbor_x == i or neighbor_y == j:
        neighbors.append([neighbor_x, neighbor_y])
  
  return neighbors

# Get all 8 neighbors of a pixel
def get_neighbors_8(i, j):
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
      
      if [neighbor_x, neighbor_y] != [i, j]:
        neighbors.append([neighbor_x, neighbor_y])
  
  return neighbors

def fill(i, j, f, f_holes_filled):
  global object_has_holes
  tags[i][j] = 1
  for neighbor in get_neighbors_8(i, j):
    m, n = neighbor

    not_visited = tags[m][n] == NO_TAG
    same_color_as_current_pixel = f_holes_filled[i][j] == f_holes_filled[m][n]

    if not_visited and same_color_as_current_pixel:
      fill(m, n, f, f_holes_filled)
      if f_holes_filled[i][j] != f[i][j] and object_has_holes == False:
        object_has_holes = True
        print(" > Found a hole in this object.\n")



file_path_was_passed = len(sys.argv) > 1

if not file_path_was_passed:
  error('Please provide an image file path')

file_path = sys.argv[1]

pgm = None 

try:
  pgm = read_pgm(file_path)
except:
  print(f'\n[ERROR] Did not find a file at {file_path}, please make sure you provided the right path.\n')
  exit(1)

tags = zeroes_matrix(pgm['height'], pgm['width'])
color = pgm['matrix']

NO_TAG = 0
height = pgm['height']
width = pgm['width']
count_objects = 0
object_has_holes = False
count_objects_with_holes = 0

f_holes_filled = fill_holes(height, width, color)

for i in range(height):
  for j in range(width):
    if tags[i][j] == NO_TAG and color[i][j] == 1:
      print(f' > Found new object at ({i}, {j})')
      count_objects += 1

      object_has_holes = False
      fill(i, j, color, f_holes_filled)

      if object_has_holes:
        count_objects_with_holes += 1

print(f'\n > Found a total of {count_objects} objects.')
print(f" > {count_objects_with_holes} have holes, while {count_objects - count_objects_with_holes} don't.")
