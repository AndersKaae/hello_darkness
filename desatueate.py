from PIL import Image, ImageEnhance

img = Image.open('356034cf-92dc-46ac-8b0a-bb3016cfd926.png')
converter = ImageEnhance.Color(img)
img2 = converter.enhance(1)
img2.save("geeks.jpg")
