import sys
import json

def log(msg):
  print(f' > {msg}')

def error(msg):
  log(msg)
  exit()

file_path = sys.argv[1]

if not file_path:
  error('Expected a file path to be provided')

input_file = open(file_path)
data = json.load(input_file)

width = data['width']
height = data['height']

matrix = [[0 for i in range(width)] for i in range(height)]

for obj in data['objects']:
  for i in range(obj['x0'], obj['xf'] + 1):
    for j in range(obj['y0'], obj['yf'] + 1):
      matrix[j][i] = 1

with open(data['output'], "w") as output_file:
  output_file.write('P1\n')
  output_file.write(f"{data['width']} {data['height']}\n")
  matrix_lines = [' '.join([str(item) for item in line]) + '\n' for line in matrix]
  output_file.writelines(matrix_lines)