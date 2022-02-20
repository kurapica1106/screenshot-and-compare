import io
import PIL
import PIL.ImageGrab

'''
f = io.StringIO("test123")
print(f, type(f))
print(f.getvalue(), type(f.getvalue()))

f = io.BytesIO(b"test123")
print(f, type(f), f.getvalue())
print(f.getvalue(), type(f.getvalue()))
'''

image_test = PIL.ImageGrab.grab()

with io.BytesIO() as output:
    image_test.save(output, format = "PNG")
    contents = output.getvalue()

with io.BytesIO(contents) as file:
    image_test2 = PIL.Image.open(file)
    image_test2.show()