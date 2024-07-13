import cv2
import os

# Caminho para a pasta de imagens
folder_path = "/home/garcez/Downloads/acnes"
output_folder_path = "/home/garcez/Downloads/acnes_processed"
os.makedirs(output_folder_path, exist_ok=True)

# Carregar o classificador Haar Cascade para detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path):
            images.append(img_path)
    return images

def process_and_save_face(image, face, output_path, size=(300, 300)):
    (x, y, w, h) = face
    # Expandir o corte ao redor do rosto para incluir mais área
    padding = 50
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + 2 * padding, image.shape[1] - x)
    h = min(h + 2 * padding, image.shape[0] - y)

    # Cortar a imagem ao redor do rosto
    face_image = image[y:y + h, x:x + w]

    # Redimensionar a imagem para o tamanho padrão
    face_image_resized = cv2.resize(face_image, size)

    # Salvar a imagem processada
    cv2.imwrite(output_path, face_image_resized)

def recognize_and_process_faces(folder, output_folder):
    images = load_images_from_folder(folder)
    
    for image_path in images:
        # Carregar a imagem
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostos
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.001, minNeighbors=110, minSize=(180, 180))
        
        if len(faces) == 0:
            continue  # Pular se nenhum rosto for detectado

        # Processar o primeiro rosto detectado (ou alterar para processar todos os rostos)
        process_and_save_face(image, faces[0], os.path.join(output_folder, os.path.basename(image_path)))

# Executar a função de reconhecimento e processamento de faces
recognize_and_process_faces(folder_path, output_folder_path)
