import sys
import numpy as np
from scipy.spatial.distance import cdist
from PIL import Image
import time

import os
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

#resmin boyutlarını göster
def get_image_resolution(image_path):
    # Resmi aç
    with Image.open(image_path) as img:
        # Resmin genişliğini ve yüksekliğini al
        width, height = img.size
        return width, height

# Özellik vektörünü almak için "avgpool" katmanının çıktısını saklamak için bir dictionary oluştur
activation = {}

# Aktivasyon fonksiyonu tanımla
def get_activation(name):
    def hook(model, input, output):
        activation[name] = output.detach()
    return hook

# Aktivasyon fonksiyonunu modelin "avgpool" katmanına kaydet
model.avgpool.register_forward_hook(get_activation("avgpool"))

# Önceden yüklenmiş özellik vektörlerini ve dosya adlarını yükle
vecs = np.load("all_vecs.npy", allow_pickle=True)
names = np.load("all_names.npy", allow_pickle=True)

uploads_folder = "uploads2/"

def single(image_id):
    #x=get_image_resolution(uploads_folder+image_id)
    #print(x)
    try:
        img = Image.open(uploads_folder + image_id)
        rotated_img = img.rotate(270) 
        img = transform(rotated_img)  # Resmi modele uygun formata dönüştür
        with torch.no_grad():
            out = model(img.unsqueeze(0))  # Modelden geçir
            vec = activation["avgpool"].numpy().squeeze()  # Özellik vektörünü al
            return [vec]
    except Exception as e:
        print("hata", e)
        return None

def find_similar(vector):
    # Tüm özellik vektörleri ile verilen resmin özellik vektörü arasındaki benzerlikleri hesapla
    distances = cdist(vector, vecs).squeeze()
    
    # En yakın 5 benzer resmin indislerini bul
    top5_indices = distances.argsort()

    # İndislere karşılık gelen resim ID'lerini al ve döndür
    similar_image_ids = [names[i] for i in top5_indices]
    return similar_image_ids

image_id = sys.argv[2]
vector = single(image_id)
similar_ids = find_similar(vector)
print(similar_ids)


#973b 1 air
#1cf5 2 kulaklik
#9898 3 air
#e33c 4 air
#665f 5 kulaklik
#d892 6 kulaklik
#86cf 7 deo
#11df 8 deo










    