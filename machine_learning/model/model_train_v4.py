import os
import torch
import torchvision
from torchvision.transforms import functional as F
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.utils.data import DataLoader, random_split
from PIL import Image

# Dataset personalizado para carregar imagens e anotações
class AcneDataset(torch.utils.data.Dataset):
    def __init__(self, root, transforms=None):
        self.root = root
        self.transforms = transforms
        self.imgs = list(sorted(os.listdir(os.path.join(root, "images"))))
        self.annotations = list(sorted(os.listdir(os.path.join(root, "annotations"))))

    def __getitem__(self, idx):
        img_path = os.path.join(self.root, "images", self.imgs[idx])
        annotation_path = os.path.join(self.root, "annotations", self.annotations[idx])
        
        img = Image.open(img_path).convert("RGB")
        boxes = []
        labels = []
        
        with open(annotation_path) as f:
            for line in f:
                xmin, ymin, xmax, ymax, label = map(int, line.split())
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(label)
        
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((len(boxes),), dtype=torch.int64)
        
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        
        if self.transforms is not None:
            img = self.transforms(img)
        
        return img, target

    def __len__(self):
        return len(self.imgs)

# Função para obter o modelo Faster R-CNN com o número de classes adequado
def get_model_instance_segmentation(num_classes):
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model

# Função para treinar o modelo
def train_model(dataset, model, device, num_epochs=10, lr=0.005, batch_size=2):
    data_loader = DataLoader(
        dataset, batch_size=batch_size, shuffle=True, num_workers=4,
        collate_fn=lambda x: tuple(zip(*x)))

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=lr, momentum=0.9, weight_decay=0.0005)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    model.to(device)
    
    for epoch in range(num_epochs):
        model.train()
        i = 0
        for images, targets in data_loader:
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
            i += 1
            print(f'Epoch: {epoch}, Iteration: {i}, Loss: {losses.item()}')

        lr_scheduler.step()

    return model

# Caminho para o diretório com as imagens e anotações
dataset_root = 'path/to/dataset'

# Inicializar dataset
dataset = AcneDataset(dataset_root)

# Dividir dataset em treino e validação
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Obter número de classes (4 severidades + 1 background)
num_classes = 5

# Inicializar modelo
model = get_model_instance_segmentation(num_classes)

# Definir dispositivo (GPU ou CPU)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# Treinar modelo
trained_model = train_model(train_dataset, model, device, num_epochs=10, lr=0.005, batch_size=2)

# Salvar o modelo treinado
torch.save(trained_model.state_dict(), 'fasterrcnn_acne_detector.pth')
