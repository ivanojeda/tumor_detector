

# **TUMORDETECTOR**
---
## 1. Descripción

El tumor cerebral es una patología cuyo tiempo de diagnóstico es clave para la supervivencia del paciente. Tradicionalmente, cada radiografía tiene que ser examinada manualmente por un especialista para detectar si hay un tumor y su posterior localización. Este proceso requiere mucho tiempo si el volumen de radiografías a analizar es elevado, cosa que suele retrasar el tiempo de diagnóstico.

**TUMORDETECTOR** es una aplicación web que agiliza este proceso con el análisis de radiografías instantáneamente mediante el uso de redes neuronales.

## 2. Instalación

### 2.1 Instalar Anaconda

Primero hay que instalar el gestor de entornos y librerías de python Anaconda a través del [siguiente enlace](https://www.anaconda.com/) y seguir todos sus pasos.

### 2.2 Crear entorno e instalar librerías

Una vez instalado Anaconda, abrimos el Anaconda Prompt (se puede acceder a él buscándolo en la barra de búsqueda de inicio de Windows) y ejecutamos los siguienes comandos:

<code>conda create --name tumordetector</code>  
<code>conda activate tumordetector</code>  
<code>conda install django numpy matplotlib</code>  
<code>pip install opencv-python</code>  
<code>pip install tensorflow</code>  

### 2.3 Descarga de la aplicación

Para descargar la aplicación acceder al siguiente enlace de Google Drive:
dd
Después, coloque la carpeta *tumor_detector* donde desée. Copie la ruta a esa carpeta y escriba los siguientes comandos en el Anaconda Prompt:  
<code>cd escriba-aqui-la-ruta</code>  
<code>python manage.py runserver</code>  

Si ha seguido los pasos correctamente, debería de aparecer un mensaje en la terminal de que el servidor se ha iniciado correctamente. Cunaod el mensaje aparezca, introduzca la siguiente dirección en su navegador:  
http://127.0.0.1:8000/

Una vez ahí podrá empezar a usar la aplicación siguiendo los pasos que se muestran a continuación:

## 3. Uso

### 3.1. Registro y acceso

En primer lugar, el usuario debe registrase siguiendo los pasos que se le indican desde la página de acceso. A continuación, deberá rellenar el formulario con su nombre y apellidos, su DNI y su e-mail y directamente le llevará a la página principal.

Si el usuario ya ha sido registrado, tan solo tiene que introducir su DNI y contraseña el la página de acceso para acceder a la página principal.

### 3.2. Gestión de pacientes

En la página principal se puede añadir un paciente pulsando **Crear Paciente**, donde se le solicitará el nombre y apellidos, el DNI, el e-mail y su sintomatología.

Además, puede gestionar sus radiografías del paciente, editar sus datos y eliminarlo de la base de datos.

### 3.3. Gestión de radiografías y diagnóstico

Una vez creado el paciente, el usuario puede gestionar sus radiografías pulsando el **Ver paciente**, que le mostrará las radiografías del paciente junto al diagnóstico de la IA.

Para añadir una radiografía, pulse **Subir radiografía** en la parte inferior de la página. A continuación, pulse  **examinar** para seleccionar el archivo de la radiografía y pulse **Subir radiografía** para efectuar su diagnóstico y añadirla a la lista del paciente.
 A continuación, puede volver a la lista o subir otra radiografía.

 ### 3.4. Cerrar sesión

Para cerrar sesión y volver a la página de acceso pulse la pestaña **Logout**.

## 4. Funcionamiento

### 4.1 Descripción general de la IA

La IA de TUMORDETECTOR se compone de 2 partes:

- Una primera fase que detecta si la radiografía contiene un tumor mediante una red neuronal residual de 50 capas (ResNet50) personalizada.

- Una segunda fase en la cual la IA analiza las imágenes con tumor y los localiza mediante una red neuronal residual en U (ResUNet).

### 4.2 ResNet50

La estructura ResNet consiste en una red convolucional cuyas capas están interconectadas más allá de sus capas adyacentes.

<image src="https://sheng-fang.github.io/img/post_img/2020-05-20-review-resnet-family/resnet_module.png" width="200">

En el caso de TUMORDETECTOR, se aplica una arquitectura **ResNet50**.

<image src="https://www.researchgate.net/publication/331364877/figure/fig3/AS:741856270901252@1553883726825/Left-ResNet50-architecture-Blocks-with-dotted-line-represents-modules-that-might-be.png" width="400">

Esta red neuronal, diseñada inicialmente para clasificar el conjunto de imágenes **ImageNet** en 1000 categorías, consta de una red neuronal convolucional, que identifica los patrones de las imágenes junto a una última capa densa que los interpreta y clasifica las imágenes en las categorías correspondientes.

<image src="https://static.geekbang.org/infoq/5c3862035fff1.png" width="400">

### 4.3 Personalización de la ResNet50

Crear una red neuronal desde 0 y entrenarla con radiografías es un proceso muy lento. Sin embargo, existe la técnica del **aprendizaje por transferencia**, que aprovecha parte de una red neuronal entrenada que efectúa una tarea parecida a la que queremos. TUMORDETECTOR se aprovecha de ello implementando la parte convolucional de la ResNet50 entrenada con ImageNet, que identifica patrones, y le añade una red neuronal densa especializada en detectar tumores. La estructura es la siguiente:

1. Capa de entrada que preprocesa las imágenes antes de entrar a la ResNet50.
2. Bloque ResNet50. Retorna 2048 filtros de 8x8.
3. Flatten del output de la ResNet50.
4. Dropout de un 20%.
5. Capa oculta de 128 neuronas. Activación ReLU.
6. Dropout del 10%.
7. Capa oculta de 92 neuronas. Activación ReLU.
8. Dropout del 10%.
9. Capa oculta de 48 neuronas. Activación ReLU.
10. Capa de salida de 1 neurona. Activación Sigmoide. Si se activa, indica presencia de tumor.

### 4.4 ResUNet

TUMORDETECTOR implementa la arquitectura ResUNet para la localización de tumores, ya que esta arquitectura no devuelve una categoría, si no que devuelve una imágen relacionada con la de entrada, que en el caso de esta aplicación es la máscara con la localización del tumor en la radiografía.

La ResUNet codifica la imágen a través de una serie de bloques convolucionales residuales y luego hace el proceso inverso para descodificarla. Los bloques residuales de codificación están conectados con los de descodificación, además de con sus capas adyacentes.

<image src="https://www.researchgate.net/profile/S-Arslanturk/publication/335348454/figure/fig4/AS:795043526881281@1566564556188/Flowchart-of-a-Res-U-Net-fully-convolutional-neural-network-for-semantic-segmentation-A.png" >








