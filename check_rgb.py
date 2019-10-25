from PIL import Image     
import os       
path = 'images/raw/'

for file in os.listdir(path): 
    if file == '.DS_Store':
        continue
    fileLoc = path+file
    img = Image.open(fileLoc)
    if img.mode != 'RGB':
        print(file+', '+img.mode)