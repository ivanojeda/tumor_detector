import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

RESNET_PATH='IA/resnet.h5'
RESUNET_PATH='IA/resunet.h5'

RESNET_BACKUP_PATH='IA/resnet_backup.h5'
RESUNET_BACKUP_PATH='IA/resunet_backup.h5'

# Meter aquí las funciones tversky o lo que sea que use la resunet.

resunet_objects=None

def tpredict(inputImgPath,outputImgPath,debug=False):
    inputImg=cv2.imread(inputImgPath)
    resnet=load_model(RESNET_PATH)
    tumor=resnet.predict(inputImg)
    if tumor<0.5:
        mask=np.zeros(shape=inputImg.shape)
    else:
        img=inputImg[np.newaxis,:,:,:]
        resunet=load_model(RESUNET_PATH,custom_objects=)
        rawmask=resunet.predict(img)[0,:,:,0]
        mask=cv2.merge((mask,mask,mask))
    outputImg=np.maximize(inputImg,mask)
    if debug==True:
        fig,ax=plt.subplots(ncols=2,figsize=(10,20))
        ax[0].imshow(inputImg)
        ax[0].set_title('input')
        ax[1].imshow(outputImg)
        ax[1].set_title('output')
    else:
        return cv2.imwrite(outputImgPath,outputImg)
          

        


