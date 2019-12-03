
from PIL import Image
import pytesseract
import argparse
import cv2
import os
from matplotlib import pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(parser.parse_args())

 
img = cv2.imread(args["image"],0)

filename = "{}.png".format(os.getpid())
print(filename)
cv2.imwrite(filename, img)


text = pytesseract.image_to_string(Image.open(filename))
print(text)
os.remove(filename)
 

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  
plt.show()