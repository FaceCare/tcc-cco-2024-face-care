import os
import pathlib
import boto3
import tensorflow as tf
import datetime

from dotenv import load_dotenv
load_dotenv()

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

if os.getenv('ENVIRONMENT') != 'PRD':
    boto3.setup_default_session(profile_name="faculdade")
s3 = boto3.client('s3')
BUCKET_CONSUMED = 'tcc-dev-consumed-bucket'
BUCKET_MODEL = 'tcc-dev-saved-model-bucket'

def download_cnn_images(severity_levels, dir_cnn_images):
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=BUCKET_CONSUMED)

    files_s3 = []
    for page in pages:
        for obj in page['Contents']:
            files_s3.append(obj['Key'])

    
    files_severity = {level: [f for f in files_s3 if str(f).startswith(f'{level}/') and f != f'{level}/'] for level in severity_levels}

    def download_list_files_s3(files: list, bucket_name: str, save_dir='', dir_cnn_images=''):
        save_dir = os.path.join(dir_cnn_images, save_dir)
        if not os.path.exists(save_dir):
            pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
            
        for f in files:
            print(f'Downloading file={f}\n')
            s3.download_file(bucket_name, f, os.path.join(save_dir, os.path.split(f)[-1]))

    for level in severity_levels:
        download_list_files_s3(files_severity[level], BUCKET_CONSUMED, level, dir_cnn_images)

# DOWNLOAD MODEL CNN IMAGES FROM S3
severity_levels = ['Severidade 0', 'Severidade 1', 'Severidade 2', 'Severidade 3', 'Severidade 4']
data_dir = 'cnn_images'
download_cnn_images(severity_levels, data_dir)

# MODEL CNN
FILE_KERAS_NAME = f"{datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S.%f')} cnn_model.keras"
OPTIMIZER = 'adam'
EPOCHS = 100 # Aqui esta um número alto, porém o código usa a estratégia de esaly stop configurada abaixo
SEED = 42
SCALE_COLOR_IMG = 1
COLOR_MODE = 'grayscale'
batch_size = 32
img_height = 512
img_width = 512

config_model = {
    "FILE_KERAS_NAME": FILE_KERAS_NAME,
    "OPTIMIZER": OPTIMIZER,
    "EPOCHS": EPOCHS,
    "SEED": SEED,
    "batch_size": batch_size,
    "img_height": img_height,
    "img_width": img_width
}
print(f'Configured model with params = \n{config_model}\n')

print('Getting training dataset ...\n')
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=SEED,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    color_mode=COLOR_MODE)

print('Getting validation dataset ...\n')
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=SEED,
  image_size=(img_height, img_width),
  batch_size=batch_size,
  color_mode=COLOR_MODE)

class_names = train_ds.class_names

print('Adding optimizer AUTOTUNE ...\n')
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

print('Data augmentation ...\n')
num_classes = len(class_names)
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

print('Sequential model ...\n')
model = Sequential([
  layers.Input(shape=(img_height, img_width, SCALE_COLOR_IMG)),
  data_augmentation,
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, (SCALE_COLOR_IMG,SCALE_COLOR_IMG), activation='relu'),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(32, (SCALE_COLOR_IMG,SCALE_COLOR_IMG), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128,activation=tf.nn.relu),
  tf.keras.layers.Dense(5, activation=tf.nn.softmax)
])

print('Compiling model ...\n')
model.compile(optimizer = OPTIMIZER,
              loss = 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

print('Setting up early stop ...')
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    accuracy = logs.get('accuracy')
    if(accuracy >= 0.85):
      print(f"\n Alcançamos {accuracy} de acurácia. Parando o treinamento!")
      self.model.stop_training = True

callbacks = myCallback()

print('Fiting model ...\n')
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=EPOCHS,
  callbacks=[callbacks]
)

print(f'Saving model {FILE_KERAS_NAME} ...\n')
model.save(FILE_KERAS_NAME, include_optimizer=False)

print(f'Uploading {FILE_KERAS_NAME} to {BUCKET_CONSUMED} ...')
s3.upload_file(FILE_KERAS_NAME, BUCKET_MODEL, FILE_KERAS_NAME)
