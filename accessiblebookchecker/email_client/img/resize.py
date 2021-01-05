from PIL import Image

img = Image.open('cc.png')
img.thumbnail((125, 125), Image.ANTIALIAS)
img.save("cc_45.png")