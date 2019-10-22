import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np
import os

IMAGE_DIR = 'orig/' # directory with original images
OUTPUT_DIR = 'new/' # directory to save augmented images to
NUM_AUG = 3 # number of new augmentations to create for each image

all_files = os.listdir(IMAGE_DIR) # get all images
images = []
for filename in all_files:
    for _ in range(NUM_AUG):
        images.append(imageio.imread(IMAGE_DIR + filename)) # put all images to be augmented in array

ia.seed(4)

# apply horizontal flip, add noise, and resize image
seq = iaa.Sequential([
    iaa.Fliplr(p=0.5), # 50% chance to flip image
    iaa.AdditiveGaussianNoise(scale=(0, 20)), # add between 0-20 gaussian noise
    iaa.Crop(percent=(0,0.2)), # crop image between 0-20%
    iaa.Resize({'height': (0.8, 1.2), 'width': (0.8, 1.2)}) # resize with and height between 80-120%
], random_order=True) # randomize order of augmentations

images_aug = seq.augment_images(images) # augment images

for i in range(len(images_aug)):
    imageio.imwrite(OUTPUT_DIR+str(i)+'.jpg', images_aug[i]) # write images to output directory
