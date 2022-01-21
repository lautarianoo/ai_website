import sys
from io import BytesIO

import tensorflow as tf
from django.core.files.uploadedfile import InMemoryUploadedFile
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from .models import ImageAI
import random
from PIL import Image
from keras.preprocessing import image

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
category = {0: 'T-shirt', 1: 'Trouser', 2:'Pullover', 3:'Dress', 4:'Coat', 5:'Sandal', 6:'Shirt', 7:'Sneaker', 8:'Bag', 9:'Ankle boot'}


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

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
      100 * np.max(predictions_array),
      class_names[true_label]),
      color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')


def neuroview(query_img, image_name):

    '''Создание модели и слоёв'''
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    '''Компилирование'''
    model.compile(
        optimizer=tf.optimizers.Adam(),  # Оптимизатор
        loss='sparse_categorical_crossentropy',  # Функция потерь
        metrics=['accuracy']  # Метрики
    )

    '''Обучение модели'''
    model.fit(train_images, train_labels, epochs=5)
    test_loss, test_acc = model.evaluate(test_images, test_labels)  # Оценка точности
    data = {
        'test_accuracy': int(test_acc * 100)
    }

    image_path = 'C:\\Users\\cerf\\Desktop\\Python\\Работы и проекты\\ai_website\\media\\' + str(image_name)
    image = tf.keras.preprocessing.image.load_img(image_path)
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    predictions = model.predict(input_arr)
    data['predictions'] = predictions
    data['predict_value'] = category.get(np.argmax(predictions))
    plot_image(0, predictions, test_labels, input_arr)
    _ = plt.xticks(rotation=45)

    print(data)
    new_model_image = ImageAI.objects.create(photo=plt.savefig('ai_image.png'))
    new_model_image.slug = f'{new_model_image.id}_{random.randint(1, 99999999)}'
    new_model_image.save()
    data['model'] = new_model_image
    return data
