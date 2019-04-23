
import numpy as np

import yaml
import json

import pynmea2
from serial import Serial

import picamera
import picamera.array

import keras
from keras.preprocessing import image
from keras.applications.xception import preprocess_input
from keras.applications.nasnet import NASNetMobile
from keras.layers import Input

#-------------------------------------------------------------------------------
#
#                   SYSTEM
#
#-------------------------------------------------------------------------------

class GeoDescribe():

    def __init__(self):

        # Buffer path
        with open('./config/image_config.yml') as f:
            self.bufferPath = yaml.safe_load(f)['buffer']

        # Modules
        self.gps = GPS()
        self.camera = Camera()
        self.model = Model()

    def snap(self):

        coordinates = self.gps.get_current_gps()
        image = self.camera.take_picture()
        imageProbabilities = self.model.predict()

        return coordinates, imageProbabilities

#-------------------------------------------------------------------------------
#
#                   GPS
#                   Camera
#                   Model
#
#-------------------------------------------------------------------------------

class GPS():

    def __init__(self):
        self.ser = Serial('/dev/ttyAMA0', 9600)

    def get_current_gps(self):

        try:
            return self._decode_buffer(self._extract_gpgga())
        except:
            return None

    def _extract_gpgga(self):

        buffer = [line for line in str(self.ser.read_all()).split('$')
                  if line.startswith("GPGGA")][-1]
        return buffer

    def _decode_buffer(self, buffer):

        buffer = buffer.replace('\\r\\n', '')
        info = pynmea2.parse(buffer)
        return info

class Camera():

    def __init__(self):

        self.camera = picamera.PiCamera()
        self.camera.resolution = (299, 299)
        self.camera.rotation = 180

    def take_picture(self):
        """Take a picture when called

        Parameters
        ----------
        self.camera: PiCamera

        Results
        -------
        output: numpy.array
            224x224x3 image
        """

#        output = np.empty((224, 224, 3), dtype=np.uint8)
        self.camera.capture('./system/buffer.jpg')

class Model():

    def __init__(self):

        with open('./config/image_config.yml') as f:
            self.modelsPaths = yaml.safe_load(f)['model']

        print("Start loading labels")
        with open(self.modelsPaths["labels"]) as f:
            self.labels = json.load(f)

        print("Start loading model")
        input_tensor = Input(shape=(224, 224, 3))
        self.model = NASNetMobile(weights=self.modelsPaths['weights'])

    def _decode_prediction(self, preds):

        return [[p,l] for p,l in zip(preds, self.labels)]

    def predict(self):
        """Predict with model for a given output

        Parameters
        ----------
        output: numpy.array
            224x224x3 image

        Results
        -------
        pred: dict
            dict with object and associated probabilities
        """

        # Load and preprocess buffer image
        img = image.load_img('./system/buffer.jpg', target_size=(224,224))
        img_arr = np.expand_dims(image.img_to_array(img), axis=0)
        x = preprocess_input(img_arr)

        # Predict
        preds = self.model.predict(x)
        print(sorted(preds))
        
        pred = self._decode_prediction(preds)
        return pred
