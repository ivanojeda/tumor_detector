from math import trunc
import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from .aiutils import focal_tversky_loss, tversky

RESNET_PATH='detector\\IA\\resnet.h5'
RESUNET_PATH='detector\\IA\\resunet.h5'

RESNET_BACKUP_PATH='detector\\IA\\resnet_backup.h5'
RESUNET_BACKUP_PATH='detector\\IA\\resunet_backup.h5'

# Meter aquí las funciones tversky o lo que sea que use la resunet.

resunet_objects={'tversky':tversky,'focal_tversky_loss':focal_tversky_loss}

def getOutputPath(inputPath):
    '''Genera el directorio de la predicción a partir de la imagen a analizar.'''
    inpathsp=inputPath.split('.')
    return inpathsp[0]+'_P.'+inpathsp[1]

def resnetImg(img):
    return img[np.newaxis,:,:,:]

def resunetImg(img):
    opimg = img/255.
    return opimg[np.newaxis,:,:,:]

def tpredict(inputImgPath,debug=False):
    '''Ejecuta la predicción.
    1) Comprueba si la imagen en 256x256, si no, reajusta la imagen a ese tamaño.
    2) Predice con la resnet si la imagen tiene tumor o no y se guarda el resultado.
    3) Dependiendo del resultado anterior:
    - Si tiene tumor, se pasa la imagen a la resunet para que devuelva la máscara del tumor predicho.
    - Si no tiene tumor, se genera una máscara vacía.
    4) Se junto la imagen con su máscara para generar la predicción y se guarda en la base de datos.
    Además, retorna un diccionario con las siguientes variables:
    - tumor: Si tiene tumor o no (0 o 1)
    - opimg: el directorio de la predicción.'''
    outputImgPath=getOutputPath(inputImgPath)
    inputImg=cv2.imread(inputImgPath)
    if inputImg.shape !=(256,256,3):
        inputImg = cv2.resize(inputImg ,dsize=(256,256),interpolation=cv2.INTER_NEAREST)
    result={}
    resnet=load_model(RESNET_PATH)
    tumor=resnet.predict(resnetImg(inputImg))[0][0]
    #print(tumor)
    if tumor<0.5:
        result['tumor']=False
        mask=np.zeros(shape=inputImg.shape)
        message='No tiene tumor.'
    else:
        result['tumor']=True
        resunet=load_model(RESUNET_PATH,custom_objects=resunet_objects)
        rawmask=resunet.predict(resunetImg(inputImg))[0,:,:,0]
        mask=cv2.merge((rawmask,rawmask,rawmask))
        mask = mask * 255
        message='Tiene tumor.'
 
    mask= mask.astype('int')
    outputImg=np.maximum(inputImg,mask)

    if debug==True:
        fig,ax=plt.subplots(ncols=3,figsize=(10,30))
        ax[0].imshow(inputImg)
        ax[0].set_title(inputImgPath,fontsize=12)
        ax[1].imshow(mask)
        ax[1].set_title('Pred Mask',fontsize=12)
        ax[2].imshow(outputImg)
        ax[2].set_title(outputImgPath,fontsize=12)
        print(message)
        plt.show()
    else:
        result['opimg']=outputImgPath.split('\\')[-1]
        cv2.imwrite(outputImgPath,outputImg.astype(np.uint8))
        return result

if __name__ == '__main__':          
    tpredict('detector\\testimgs\\TCGA_CS_4944_20010208_13.tif') #tumor
    #tpredict('detector\\testimgs\\TCGA_CS_4944_20010208_17.tif',debug=True) #no tumor

