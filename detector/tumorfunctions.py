import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

RESNET_PATH='IA/resnet.h5'
RESUNET_PATH='IA/resunet.h5'

RESNET_BACKUP_PATH='IA/resnet_backup.h5'
RESUNET_BACKUP_PATH='IA/resunet_backup.h5'

# Meter aquí las funciones tversky o lo que sea que use la resunet.

resunet_objects=None

def tpredict(inputImgPath,outputImgPath):
    image=cv2.imread(inputImgPath)
    resnet=load_model(RESNET_PATH)
    tumor=resnet.predict(image)
    if tumor<0.5:
        mask=np.zeros(shape=image.shape)
    else:
        resunet=load_model(RESUNET_PATH,custom_objects=)
        mask=resunet.predict(image)
    return cv2.imwrite(outputImgPath,pred2)
          

        


