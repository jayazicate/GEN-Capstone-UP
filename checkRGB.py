from PIL import Image     
import os       
path = 'images/raw/'

for file in os.listdir(path): 
    # extension = file.split('.')[-1]
    if file == '.DS_Store':
        continue
    fileLoc = path+file
    img = Image.open(fileLoc)
    #print(file)
    if img.mode != 'RGB':
        print(file+', '+img.mode)