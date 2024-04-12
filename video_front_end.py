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

uploads_folder = "uploads/"

def single(image_id):
    try:
        img = Image.open(uploads_folder + image_id)
        img = transform(img)  # Resmi modele uygun formata dönüştür
        with torch.no_grad():
            out = model(img.unsqueeze(0))  # Modelden geçir
            vec = activation["avgpool"].numpy().squeeze()  # Özellik vektörünü al
            return [vec]
    except Exception as e:
        print("hata", e)
        return None

def find_similar(vector):
    # Resim ID'sine karşılık gelen özellik vektörünü bul
    #idx = np.where(names == image_id)[0]
    #if len(idx) == 0:
    #    return []  # Eğer geçersiz bir resim ID'si verildiyse boş listeyi döndür
    #target_vec = vecs[idx]

    # Tüm özellik vektörleri ile verilen resmin özellik vektörü arasındaki benzerlikleri hesapla
    distances = cdist(vector, vecs).squeeze()
    
    # En yakın 5 benzer resmin indislerini bul
    top5_indices = distances.argsort()[1:3]

    # İndislere karşılık gelen resim ID'lerini al ve döndür
    similar_image_ids = [names[i] for i in top5_indices]
    return similar_image_ids

# Örnek bir kullanım
#image_id = "ce98f689f6fba91893733463a96258a6"  # Aranacak resmin ID'si
#similar_ids = find_similar(image_id)
#print("Benzer resim ID'leri:", similar_ids)


#37a6 portakal
#c74b portakal
#600c portakal
#5ceb ispanak
#58a6 ispanak
#5f90 ispanak


# Komut satırı argümanını al
#if len(sys.argv) != 2:
#    print("Kullanım: python3 script.py <resim_id>")
#    sys.exit(1)

image_id = sys.argv[2]
vector = single(image_id)
similar_ids = find_similar(vector)
print("Benzer resim ID'leri:", similar_ids)
#print("vector:", vector)






    