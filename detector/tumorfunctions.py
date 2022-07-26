import tensorflow as tf

from tf.keras.models import load_model

RESNET_PATH=''
RESUNET_PATH=''

def __loadimage(imagedata):
    imagetensor=None # WIP
    return imagetensor

def __saveimage(imagetensor):
    imagedata=None # WIP
    return imagedata

def tpredict(imagedata):
    image=__loadimage(imagedata)
    model1=load_model(RESNET_PATH)
    pred1=model.predict(imagetensor)
    if pred1<0.5:
        model2=load_model(RESUNET_PATH)
        pred2=model.predict(imagetensor)
        _saveimage()
        


