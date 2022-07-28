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

def getOutputPath(inputPath):
    inpathsp=inputPath.split('.')
    return inpathsp[0]+'_P.'+inpathsp[1]

def resnetImg(img):
    imsize=256
    if img.shape!=(256,256,3):
        opimg = cv2.resize(img ,dsize=(imsize,imsize),interpolation=cv2.INTER_NEAREST)
    else: 
        opimg = img
    return img[np.newaxis,:,:,:]

def resunetImg(img):
    imsize=128
    if img.shape!=(256,256,3):
        opimg = cv2.resize(img ,dsize=(imsize,imsize),interpolation=cv2.INTER_NEAREST)
    else:
        opimg=img
    opimg=opimg/255.
    return img[np.newaxis,:,:,:]

def tpredict(inputImgPath,debug=False):
    outputImgPath=getOutputPath(inputImgPath)
    inputImg=cv2.imread(inputImgPath)
    resnet=load_model(RESNET_PATH)
    tumor=resnet.predict(resnetImg(inputImg))
    if tumor<0.5:
        mask=np.zeros(shape=inputImg.shape)
    else:
        resunet=load_model(RESUNET_PATH,custom_objects=resunet_objects)
        rawmask=resunet.predict(resunetImg(inputImg))[0,:,:,0]
        mask=cv2.merge((rawmask,rawmask,rawmask))
    outputImg=np.maximum(inputImg,mask)
    if debug==True:
        fig,ax=plt.subplots(ncols=2,figsize=(10,20))
        ax[0].imshow(inputImg)
        ax[0].set_title(inputImgPath)
        ax[1].imshow(outputImg)
        ax[1].set_title(outputImgPath)
        plt.show()
    else:
        return cv2.imwrite(outputImgPath,outputImg)
          
tpredict('detector\\testimgs\\TCGA_CS_4944_20010208_13.tif',debug=True)
     


