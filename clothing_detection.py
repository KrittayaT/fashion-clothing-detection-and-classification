# -*- coding: utf-8 -*-
"""clothing-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1odmoUsyVUmP-qEQBdSRQ9wxgLi3qnfUj
"""

!pip install ultralytics==8.0.128

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import json
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import cv2
import shutil
import tqdm
import glob
import torch
from ultralytics import YOLO
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

# mount ti google drive
from google.colab import drive
drive.mount('/content/drive')

# load model
model = torch.load(f='/content/drive/MyDrive/model_it4.pt')

images_path = '/content/drive/MyDrive/person_images.zip (Unzipped Files)/2023-05-31'

len(os.listdir(images_path))

def check_detection(imgs_path):
  ims = imgs_path.split('/content/drive/MyDrive/person_images.zip (Unzipped Files)/2023-05-31/')[1]
  #i = model_2.predict(source=images_path+'/'+ims, conf=0.25, save=True, line_width=2, classes=[0,1,2,3,4,5,6,7,8,10])
  i = model.predict(source=images_path+'/'+ims, conf=0.25, save=True, line_width=2)
  #c=1
  plt.figure(figsize=(5,5))
  im = plt.imread('runs/detect/predict/'+ims)
  ori_im = plt.imread(images_path+'/'+ims)
  plt.axis('off')
  plt.imshow(im)

  total_annotations = []
  class_conf = []
  class_pred = []
  total_labels_box =[]
  labels = ['sunglass','hat','jacket','shirt','pants','shorts','skirt','dress','bag','shoe','mask']
  result = i[0]
  for box in result.boxes:
      class_id = result.names[box.cls[0].item()]
      cords = box.xywhn[0].tolist()
      cords = [x for x in cords]
      conf = round(box.conf[0].item(), 2)
      #print("Object type:", class_id)
      #print("Coordinates:", cords)
      #print("Probability:", conf)

      class_index = labels.index(str(class_id))
      class_pred.append(class_id)
      labels_box = str(class_index) + " " + str(cords[0]) + " " + str(cords[1]) + " " + str(cords[2]) + " " + str(cords[3])
      total_labels_box.append(labels_box)
      total_annotations.append(labels_box)
      class_conf.append(str(class_id)+" "+str(conf))
      #print(labels_box)

      #print("---")

      # crop image from yolo format
      dh, dw , _= ori_im.shape
      x_center = cords[0]
      y_center = cords[1]
      w = cords[2]
      h = cords[3]
      x_center = round(x_center * dw)
      y_center = round(y_center * dh)
      w = round(w * dw)
      h = round(h * dh)
      x = round(x_center - w / 2)
      y = round(y_center - h / 2)

      #if conf >= 0.25:
        #print(class_id)
        #print(class_pred)
        #crop_img = ori_im[y:y+h, x:x+w]
        #plt.imshow(crop_img)

  return class_conf,total_labels_box

img = random.sample(os.listdir(images_path),1)
#img

check_detection(os.path.join(images_path,img[0]))