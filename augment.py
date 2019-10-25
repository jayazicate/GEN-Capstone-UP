import imageio
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os
import csv

IMAGE_DIR = 'images/raw/' # directory with original images
OUTPUT_DIR = 'images/augmented/' # directory to save augmented images to
NUM_AUG = 3 # number of new augmentations to create for each image
LABELS_INPUT = 'raw_labels.csv'
LABELS_OUTPUT = 'augmented_labels.csv'

ia.seed(4)

all_bboxes = {}
with open(LABELS_INPUT) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader) # skip header line
    for row in reader:
        bbox = row[4:] + [row[3]]
        if row[0] in all_bboxes:
            all_bboxes[row[0]].append(bbox)
        else:
            all_bboxes[row[0]] = [bbox]

with open(LABELS_OUTPUT, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])

# apply horizontal flip, add noise, and resize image
seq = iaa.Sequential([
    iaa.Fliplr(p=0.5), # 50% chance to flip image
    iaa.AdditiveGaussianNoise(scale=(0, 20)), # add between 0-20 gaussian noise
    iaa.Resize({'height': (0.8, 1.2), 'width': (0.8, 1.2)}), # resize width and height between 80-120%
    iaa.Add((-40, 40))
], random_order=True) # randomize order of augmentations

progress = 1
all_files = os.listdir(IMAGE_DIR) # get all images
all_files.sort()
for filename in all_files:
    image = imageio.imread(IMAGE_DIR + filename)

    bboxes = []
    for bbox in all_bboxes[filename]:
        bboxes.append(BoundingBox(x1=int(bbox[0]), y1=int(bbox[1]), x2=int(bbox[2]), y2=int(bbox[3]), label=bbox[4]))
    bboxes_on_image = BoundingBoxesOnImage(bboxes, shape=image.shape)

    image_batch = []
    bbox_batch = []
    for _ in range(NUM_AUG):
        image_batch.append(image) # put all images to be augmented in array
        bbox_batch.append(bboxes_on_image)

    images_aug, bbs_aug = seq(images=image_batch, bounding_boxes=bbox_batch) # augment images

    new_bboxes = []
    imageio.imwrite(OUTPUT_DIR + filename, image) # write original image to output directory
    image_height = bboxes_on_image.shape[0]
    image_width = bboxes_on_image.shape[1]
    for bb in bboxes_on_image.bounding_boxes:
        new_bboxes.append([filename, image_width, image_height, bb.label, bb.x1, bb.y1, bb.x2, bb.y2])

    for i in range(len(images_aug)):
        out_filename = str(i) + '_' + filename
        out_filepath = OUTPUT_DIR + out_filename
        out_image_height = bbs_aug[i].shape[0]
        out_image_width = bbs_aug[i].shape[1]
        imageio.imwrite(out_filepath, images_aug[i]) # write augmented image to output directory
        for bb in bbs_aug[i].bounding_boxes:
            new_bboxes.append([out_filename, out_image_width, out_image_height, bb.label, int(round(bb.x1)), int(round(bb.y1)), int(round(bb.x2)), int(round(bb.y2))])
    
    with open(LABELS_OUTPUT, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for bb in new_bboxes:
            writer.writerow(bb)
    
    print('Progress: ' + str(progress) + '/' + str(len(all_files)), end = '\r', flush=True) # report progress of augmentation
    progress += 1