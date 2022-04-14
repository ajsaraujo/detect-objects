def log(msg):
  print(f' > {msg}')

def read_int(prompt):
  return int(input(f' > {prompt} '))

def read_object(index):
  description = ''

  if index == 1:
    description = '1st'
  elif index == 2:
    description = '2nd'
  elif index == 3:
    description = '3rd'
  else:
    description = f'{index}th'
  
  log(f'{description} object')

  x0 = read_int('x0:')
  y0 = read_int('y0:')

  xf = read_int('xf:')
  yf = read_int('yf:')

  return [[x0, y0], [xf, yf]]

log("Let's generate an image...")
log("...but first, I need to ask some questions:")

width = read_int("What is the width of the image?")
height = read_int("What is the height of the image?")

num_of_objects = read_int("How many objects will the image have?")

log("Cool. Now, let's find out what the objects look like.")

objects = [read_object(i) for i in range(num_of_objects)]

