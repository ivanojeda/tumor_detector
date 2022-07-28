import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from aiutils import focal_tversky_loss, tversky

RESNET_PATH='detector\\IA\\resnet.h5'
RESUNET_PATH='detector\\IA\\resunet.h5'

RESNET_BACKUP_PATH='detector\\IA\\resnet_backup.h5'
RESUNET_BACKUP_PATH='detector\\IA\\resunet_backup.h5'

# Meter aquí las funciones tversky o lo que sea que use la resunet.

resunet_objects={'tversky':tversky,'focal_tversky_loss':focal_tversky_loss}

def tpredict(inputImgPath,outputImgPath=None,debug=False):
    inputImg=cv2.resize(cv2.imread(inputImgPath),dsize=(128,128),interpolation=cv2.INTER_NEAREST)/255.
    #resnet=load_model(RESNET_PATH)
    #tumor=resnet.predict(inputImg)
    tumor=1
    if tumor<0.5:
        mask=np.zeros(shape=inputImg.shape)
    else:
        img=inputImg[np.newaxis,:,:,:]
        resunet=load_model(RESUNET_PATH,custom_objects=resunet_objects)
        rawmask=resunet.predict(img)[0,:,:,0]
        mask=cv2.merge((rawmask,rawmask,rawmask))
    outputImg=np.maximum(inputImg,mask)
    if debug==True:
        fig,ax=plt.subplots(ncols=2,figsize=(10,20))
        ax[0].imshow(inputImg)
        ax[0].set_title('input')
        ax[1].imshow(outputImg)
        ax[1].set_title('output')
        plt.show()
    else:
        return cv2.imwrite(outputImgPath,outputImg)
          
tpredict('detector\\testimgs\\TCGA_CS_4944_20010208_13.tif',debug=True)
     


