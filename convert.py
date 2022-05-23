from pathlib import Path
from PIL import Image

# Convert PNG to PBM P1
ASCII_BITS = '1', '0'
imagepath = Path('objects_3.png')

# Convert image to bitmap
img = Image.open(imagepath).convert('1') 
width, height = img.size

# Convert image data to a list of ASCII bits
data = [ASCII_BITS[bool(val)] for val in img.getdata()]

# Convert that to 2D list (list of character lists)
data = [data[offset: offset+width] for offset in range(0, width*height, width)]

with open(f'{imagepath.stem}.pbm', 'w') as file:
    file.write('P1\n')
    file.write(f'{width} {height}\n')

    for row in data:
        file.write(' '.join(row) + '\n')