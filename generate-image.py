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

file = open(file_path)
data = json.load(file)

print(data)