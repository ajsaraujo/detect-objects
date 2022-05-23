# detect-objects

Image Processing (COMP0432) project. We created a script that detects objects in PBM images and also tells apart objects that have holes in them.

- `convert.py` is a script that converts PNG images to PBM P1 images - we used it to generate our input images.
- `detect-objects.py` is the object detecting script.

Both of them take an image as a command line argument. You'll need Python 3+ installed.

```
$ python convert.py input.png
$ python detect-objects.py images/objects_1.pbm
```
