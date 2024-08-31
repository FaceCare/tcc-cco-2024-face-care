import logging
import tempfile
import os
import numpy as np
from fastapi import UploadFile
import tensorflow as tf
from PIL import Image
from skimage.color import rgb2gray
from skimage.io import imread

class AcneService:

    def __init__(self) -> None:
        pass

    def preprocess_image(self, image_path):
        img = Image.open(image_path)
        
        if img.mode == 'RGB':
            img = img.convert('L')
        
        img = img.resize((512, 512))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict_image_severity_and_confidence(self, image_path, model_path, img_size=(512, 512)) -> int:

        def softmax_v2(x):
            return tf.nn.softmax(x)
        
        tf.keras.utils.get_custom_objects().update({'softmax_v2': tf.keras.layers.Activation(softmax_v2)})

        model = tf.keras.models.load_model(model_path, custom_objects={'softmax_v2': softmax_v2})
        image = self.preprocess_image(image_path)
        predictions = model.predict(image)
        predicted_class = np.argmax(predictions, axis=1)
        confidence = float(np.max(predictions, axis=1)[0]) * 100
        confidence = f'{confidence:.2f}%'

        return predicted_class[0], confidence

    def get_acne_report(self, photo: UploadFile, last_model_keras_name: str):
        logging.info(f'Generating acne report for {photo.filename}...')
        
        try:
            tmp_dir = tempfile.gettempdir()            
            last_model_path = os.path.join(tmp_dir, last_model_keras_name)

            photo_path = os.path.join(tmp_dir, photo.filename)
            with open(photo_path, 'wb') as tmp_file:
                tmp_file.write(photo.file.read())

            severity, confidence = self.predict_image_severity_and_confidence(photo_path, last_model_path)

            # TODO: save in bucket raw to use later
            os.remove(photo_path)

            severity_messages = {
                0: 'Você não possuí acne, tudo normal por aqui!',
                1: 'Você possuí acne leve (grau 1), recomendamos buscar um dermatologista!',
                2: 'Você possuí acne moderada (grau 2), recomendamos buscar um dermatologista!',
                3: 'Você possuí acne grave (grau 3), recomendamos buscar um dermatologista!',
                4: 'Você possuí acne muito grave (grau 4), recomendamos buscar um dermatologista!'
            }

            report_msg = severity_messages.get(severity, 'Severidade desconhecida. Por favor, consulte um dermatologista.')

            return {'status': severity != 0, 'severity': severity, 'confidence': confidence, 'report': report_msg}
        
        except Exception as e:
            if os.path.exists(photo_path):
                os.remove(photo_path)
            raise e
