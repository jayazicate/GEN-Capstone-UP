import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from PIL import Image
import pytesseract
import numpy as np
import csv
import cv2
import os

# suppress tensorflow output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# directory of images to be grouped
source_dir = 'test_photos/'

# directories for images to be put into
sf_dir = 'split_storefronts/'
faces_dir = 'split_faces/'
ads_dir = 'split_ads/'
other_dir = 'split_other/'

# pretrained tensorflow models to use
group_model = 'group_images_96.h5'
storefront_model = 'classify_storefronts_96.h5'
faces_model = 'classify_faces_96.h5'

# csv to output information to
output_csv = 'output.csv'

# dimensions to rescale images to
input_width = 96
input_height = 96

# get predictions for images in a directory using a specified model
def generate_predictions_from_dir(pre_trained_model, model_name, ims_dir):
    im_names = os.listdir(ims_dir)
    ims = []
    # load and resize images
    for im_name in im_names:
        if not (im_name.endswith('.jpg') or im_name.endswith('.jpeg')):
                continue
        im = cv2.imread(source_dir + im_name)
        im_resize = cv2.cvtColor(cv2.resize(im, dsize=(input_width, input_height), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
        ims.append(im_resize)

    ims = np.array(ims)
    ims = tf.keras.applications.mobilenet_v2.preprocess_input(ims) # preprocess images

    # extract feature vectors
    feature_vectors = pre_trained_model.predict(ims)

    # get predictions from feature vectors
    model = tf.keras.models.load_model(model_name)
    predictions = model.predict(feature_vectors)
    return predictions, im_names

# define model for extracting feature vectors
pre_trained_model = keras.applications.mobilenet_v2.MobileNetV2(
    input_shape=(input_width, input_height, 3), 
    include_top=False,
    weights='imagenet',
    pooling=None)
last_output = pre_trained_model.output
x = layers.Flatten()(last_output)
pre_trained_model = Model(pre_trained_model.input, x)

print('------------------------')
print('Grouping images...')

grouping_predictions, grouping_im_names = generate_predictions_from_dir(pre_trained_model, group_model, source_dir)

labels = [other_dir, ads_dir, faces_dir, sf_dir]
count = [0, 0, 0, 0]
# copy images to new directories based on their classifications
for i, prediction in enumerate(grouping_predictions):
    print('Progress: ' + str(i+1) + '/' + str(len(grouping_predictions)), end = '\r', flush=True)
    label = np.argmax(prediction)
    count[label] += 1
    dest_dir = labels[label]
    if label != 0:
        os.system('cp ' + source_dir + grouping_im_names[i] + ' ' + dest_dir + grouping_im_names[i])

print('')
# print grouping information
print('Total Images:', len(grouping_im_names))
print('Storefronts:', count[3])
print('Faces:', count[2])
print('Advertisements:', count[1])
print('Other:', count[0])

print('------------------------')
print('Creating CSV file...')

storefront_predictions, storefront_im_names = generate_predictions_from_dir(pre_trained_model, storefront_model, sf_dir)    

faces_predictions, faces_im_names = generate_predictions_from_dir(pre_trained_model, faces_model, faces_dir)

# write model output to csv
with open(output_csv, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['Image Name', 'License ID', 'Category', 'Output'])

    total_count = count[1] + count[2] + count[3] + 1
    cur = 1

    # write risk scores for storefronts
    for i, prediction in enumerate(storefront_predictions):
        print('Progress: ' + str(cur) + '/' + str(total_count), end = '\r', flush=True)
        im_name = storefront_im_names[i]
        lic_id = im_name.split('_')[0]
        output = prediction[0]
        category = 'Storefront'
        writer.writerow([im_name, lic_id, category, output])
        cur+=1

    # write risk scores for faces
    for i, prediction in enumerate(faces_predictions):
        print('Progress: ' + str(cur) + '/' + str(total_count), end = '\r', flush=True)
        im_name = faces_im_names[i]
        lic_id = im_name.split('_')[0]
        output = prediction[0]
        category = 'Face'
        writer.writerow([im_name, lic_id, category, output])
        cur+=1

    # write text from ads
    for filename in os.listdir(ads_dir):
        print('Progress: ' + str(cur) + '/' + str(total_count), end = '\r', flush=True)
        im_name = filename
        lic_id = im_name.split('_')[0]
        category = 'Ad'
        output = pytesseract.image_to_string(Image.open(ads_dir + filename))
        writer.writerow([im_name, lic_id, category, output])
        cur+=1

print('Progress: ' + str(cur) + '/' + str(total_count))
print('Successfully created CSV file:', output_csv)