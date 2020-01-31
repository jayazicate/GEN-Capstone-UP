import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
import numpy as np
import cv2
import os

source_dir = 'test_photos/'
sf_dir = 'test_storefronts/'
faces_dir = 'test_faces/'
ads_dir = 'test_ads/'
other_dir = 'test_other/'

input_width = 96
input_height = 96

im_names = os.listdir(source_dir)

ims =[]
for im_name in im_names:
    if not (im_name.endswith('.jpg') or im_name.endswith('.jpeg')):
            continue
    im = cv2.imread(source_dir + im_name)
    im_resize = cv2.cvtColor(cv2.resize(im, dsize=(input_width, input_height), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
    ims.append(im_resize)

ims = np.array(ims)
ims = tf.keras.applications.mobilenet_v2.preprocess_input(ims)

pre_trained_model = keras.applications.mobilenet_v2.MobileNetV2(
    input_shape=(input_width, input_height, 3), 
    include_top=False,
    weights='imagenet',
    pooling=None)
last_output = pre_trained_model.output
x = layers.Flatten()(last_output)
pre_trained_model = Model(pre_trained_model.input, x)

feature_vectors = pre_trained_model.predict(ims)
model = tf.keras.models.load_model('group_images_96.h5')
predictions = model.predict(feature_vectors)

labels = [other_dir, ads_dir, faces_dir, sf_dir]
count = [0, 0, 0, 0]
for i, prediction in enumerate(predictions):
    count[np.argmax(prediction)] += 1
    dest_dir = labels[np.argmax(prediction)]
    os.system('cp ' + source_dir + im_names[i] + ' ' + dest_dir + im_names[i])

print('------------------------')
print('Total Images:', len(ims))
print('Storefronts:', count[3])
print('Faces:', count[2])
print('Advertisements:', count[1])
print('Other:', count[0])