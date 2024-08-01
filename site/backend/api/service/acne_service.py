import logging
import tempfile
import os
import numpy as np
import shutil
from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from datetime import datetime
import tensorflow as tf
from PIL import Image

from integrations.storage_s3 import StorageS3
from enums.bucket_s3_enum import BucketS3Enum

class AcneService:

    def __init__(self) -> None:
        pass

    def preprocess_image(self, image_path):
        img = Image.open(image_path).convert('RGB')
        img = img.resize((512, 512))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict_image_severity(self, image_path, model_path, img_size=(128, 128)) -> int:

        def softmax_v2(x):
            return tf.nn.softmax(x)
        
        tf.keras.utils.get_custom_objects().update({'softmax_v2': tf.keras.layers.Activation(softmax_v2)})

        model = tf.keras.models.load_model(model_path, custom_objects={'softmax_v2': softmax_v2})
        image = self.preprocess_image(image_path)
        predictions = model.predict(image)
        predicted_class = np.argmax(predictions, axis=1)
        return predicted_class[0]

    def get_acne_report(self, photo: UploadFile):
        logging.info(f'Generating acne report for {photo.filename}...')
        storage_s3 = StorageS3(bucket_name=BucketS3Enum.BUCKET_TRAINED_MODEL.value)
        files_s3 = storage_s3.list_all_files()

        def extract_datetime_from_filename(filename):
            try:
                timestamp_str = filename.split(' cnn_model.h5')[0]
                return datetime.strptime(timestamp_str, '%d-%m-%Y %H-%M-%S.%f')
            except ValueError as e:
                logging.error(f'Error parsing datetime from filename {filename}: {e}')
                return datetime.min

        try:
            if files_s3:
                # Ordenar arquivos pelo timestamp no nome
                files_s3.sort(key=extract_datetime_from_filename, reverse=True)
                last_model_name = os.path.split(files_s3[0])[-1]
            else:
                raise HTTPException(404, 'No model.h5 found in bucket...')

            tmp_dir = tempfile.mkdtemp(prefix='last_model_h5')
            last_model_path = os.path.join(tmp_dir, last_model_name)
            storage_s3.download(last_model_name, last_model_path)

            with open(os.path.join(tmp_dir, photo.filename), 'wb') as tmp_file:
                tmp_file.write(photo.file.read())
            
            severity = self.predict_image_severity(os.path.join(tmp_dir, photo.filename), last_model_path)

            shutil.rmtree(tmp_dir)

            severity_messages = {
                0: 'Você não possuí acne, tudo normal por aqui!',
                1: 'Você possuí acne leve (grau 1), recomendamos buscar um dermatologista!',
                2: 'Você possuí acne moderada (grau 2), recomendamos buscar um dermatologista!',
                3: 'Você possuí acne grave (grau 3), recomendamos buscar um dermatologista!',
                4: 'Você possuí acne muito grave (grau 4), recomendamos buscar um dermatologista!'
            }

            report_msg = severity_messages.get(severity, 'Severidade desconhecida. Por favor, consulte um dermatologista.')

            return {'status': severity != 0, 'severity': severity, 'report': report_msg}
        
        except Exception as e:
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            raise e
