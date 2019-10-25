# GEN-Capstone-UP
GEN-Capstone-UP is the University of Portland capstone project for Global Emancipation Network.

## Installation
### Dependencies
This project requires TensorFlow 1.14. Install with pip:

```bash
pip install tensorflow==1.14
```

### TensorFlow Object Detection API
This project uses the [TensorFlow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection) for object detection. To install the API follow the [installation guide](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md).

## Usage
### Image Classification
To classify images, copy the contents of the `GEN-Capstone-UP/object_detection` directory from this project into the `models/research/object_detection` directory of the TensorFlow Object Detection API. This project uses the [ssd\_mobilenet\_v1\_coco](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2018_01_28.tar.gz) model from the [TensorFlow  detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for object detection. Copy the downloaded model to the `models/research/object_detection` directory of the TensorFlow Object Detection API. Put images to be classified in the `models/research/object_detection/test_images` directory of the TensorFlow Object Detection API. Classify the images by running:

```bash
python classify_images.py
```