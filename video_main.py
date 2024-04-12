import os
from PIL import Image
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import torchvision.models
import torch
import torch.nn as nn
import torchvision
from torchvision import transforms

# ResNet-18 modelini yükle
model = torchvision.models.resnet18(weights="DEFAULT")
model.eval()

# Transformasyonları tanımla
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Özellik vektörünü almak için "avgpool" katmanının çıktısını saklamak için bir dictionary oluştur
activation = {}

# Aktivasyon fonksiyonu tanımla
def get_activation(name):
    def hook(model, input, output):
        activation[name] = output.detach()
    return hook

# Aktivasyon fonksiyonunu modelin "avgpool" katmanına kaydet
model.avgpool.register_forward_hook(get_activation("avgpool"))

# Yeni resimlerin yüklendiği klasör
uploads_folder = "uploads/"

# Önceden çıkarılmış özellik vektörleri ve dosya adlarını yükle (eğer varsa)
if os.path.exists("all_vecs.npy"):
    all_vecs = np.load("all_vecs.npy")
else:
    all_vecs = None

if os.path.exists("all_names.npy"):
    all_names = list(np.load("all_names.npy"))
else:
    all_names = []

# Yeni yüklenen resimleri işle
new_images = [img for img in os.listdir(uploads_folder) if img not in all_names]
for file in new_images:
    try:
        img = Image.open(uploads_folder + file)
        img = transform(img)  # Resmi modele uygun formata dönüştür
        with torch.no_grad():
            out = model(img.unsqueeze(0))  # Modelden geçir
            vec = activation["avgpool"].numpy().squeeze()  # Özellik vektörünü al
            # Yeni özellik vektörünü önceki vektörlerle birleştir
            if all_vecs is None:
                all_vecs = vec.reshape(1, -1)
            else:
                all_vecs = np.vstack([all_vecs, vec])
            all_names.append(file)  # Dosya adını listeye ekle
    except Exception as e:
        print("hata", e)
        continue

# Son özellik vektörlerini ve dosya adlarını kaydet
np.save("all_vecs.npy", all_vecs)
np.save("all_names.npy", all_names)