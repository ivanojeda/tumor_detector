import numpy as np
import cv2
import tensorflow as tf
from tf.keras.models import load_model

RESNET_PATH='resnet.h5'
RESUNET_PATH='resunet.h5'

RESNET_BACKUP_PATH='resnet_backup.h5'
RESUNET_BACKUP_PATH='resunet_backup.h5'

def tpredict(inputImgPath,outputImgPath):
    image=cv2.imread(inputImgPath)
    model1=load_model(RESNET_PATH)
    pred1=model1.predict(image)
    if pred1<0.5:
        pred2=np.zeros(shape=image.shape)
    else:
        model2=load_model(RESUNET_PATH)
        pred2=model2.predict(image)
    return cv2.imwrite(outputImgPath,pred2)
          

        


