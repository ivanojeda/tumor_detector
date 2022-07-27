import numpy as np
import cv2
import tensorflow as tf
from tf.keras.models import load_model

RESNET_PATH='resnet.h5'
RESUNET_PATH='resunet.h5'

RESNET_BACKUP_PATH='resnet_backup.h5'
RESUNET_BACKUP_PATH='resunet_backup.h5'

def __loadimage(img_binstr):
    image_np = np.from_buffer(img_binstr, dtype=np.uint8) # Get a 1d-array of an image
    imagetensor=cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    return imagetensor

def __saveimage(imagetensor):
    imagedata=imagetensor.dumps()
    return imagedata

def tpredict(imagedata):
    image=__loadimage(imagedata)
    model1=load_model(RESNET_PATH)
    pred1=model1.predict(imagetensor)
    if pred1<0.5:
        pred2=np.zeros(shape=(256,256,3))
    else:
        model2=load_model(RESUNET_PATH)
        pred2=model2.predict(imagetensor)
        return __saveimage(pred2)
          

        


