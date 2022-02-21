import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from .models import ImageAI
import random
import cv2

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names =  ['Футболка', 'Штаны', 'Свитер', 'Платье', 'Пальто',
               'Сандали', 'Рубашка', 'Кроссовки', 'Сумка', 'Ботильоны']
category = {0: 'T-shirt', 1: 'Trouser', 2:'Pullover', 3:'Dress', 4:'Coat', 5:'Sandal', 6:'Shirt', 7:'Sneaker', 8:'Bag', 9:'Ankle boot'}
category_russian = {0: 'Футболка', 1: 'Штаны', 2:'Свитер', 3:'Платье', 4:'Пальто', 5:'Сандали', 6:'Рубашка', 7:'Кроссовки', 8:'Сумка', 9:'Ботильоны'}

'''Отображение'''
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}%".format(class_names[predicted_label],
      100 * np.max(predictions_array)),
      color=color)
  plt.savefig('media/saved_figure.png', dpi=100)



from PIL import Image, ImageFilter


def imageprepare(argv):
    im = Image.open(argv).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas

    # newImage.save("sample.png

    tv = list(newImage.getdata())  # get pixel values

    # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
    tva = [(255 - x) * 1.0 / 255.0 for x in tv]
    return tva

def neuroview(model_image):

    '''Создание модели и слоёв'''
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    print(os.path.abspath(os.path.dirname(__file__)))
    '''Компилирование'''
    model.compile(
        optimizer=tf.optimizers.Adam(),  # Оптимизатор
        loss='sparse_categorical_crossentropy',  # Функция потерь
        metrics=['accuracy']  # Метрики
    )

    '''Обучение модели'''
    model.fit(train_images, train_labels, epochs=4)
    test_loss, test_acc = model.evaluate(test_images, test_labels)  # Оценка точности
    data = {
        'test_accuracy': int(test_acc * 100)
    }

    image_path = 'C:/Users/cerf/Desktop/Python/Готовые проекты и работы/ai_website' + str(model_image.photo.url)
    image = tf.keras.preprocessing.image.load_img(image_path)
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    test_img_array = input_arr / 255.0  # normalize
    test_img_array = tf.image.rgb_to_grayscale(test_img_array)  # will return shape (28, 28, 1)
    test_img_array = tf.squeeze(test_img_array, axis=-1)  # shape is (28, 28)
    test_img_array = tf.expand_dims(test_img_array, axis=0)  # shape: (1, 28, 28)

    predictions = model.predict(test_img_array)
    data['predictions'] = predictions
    data['predict_value'] = category_russian.get(np.argmax(predictions))
    plot_image(0, predictions, test_labels, input_arr)
    _ = plt.xticks(rotation=45)
    data['percent'] = 100*np.max(predictions)

    image_path = "saved_figure.png"
    new_model_image = ImageAI.objects.create(photo=image_path)
    new_model_image.slug = f'{new_model_image.id}_{random.randint(1, 99999999)}'
    new_model_image.save()
    data['model'] = new_model_image
    return data
