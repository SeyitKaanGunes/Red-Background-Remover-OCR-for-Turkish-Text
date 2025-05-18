# Gerekli kurulumlar (Colab ortamı için)
!apt-get update
!apt-get install -y tesseract-ocr tesseract-ocr-tur
!pip install opencv-python-headless pytesseract matplotlib

import cv2
import pytesseract
import numpy as np
import io
from PIL import Image
import matplotlib.pyplot as plt
from google.colab import files

def remove_red_background(image):
    """
    Kırmızı arka planı maskeleyip, beyaz metni ayıklamak için renk tabanlı maskeleme.
    """
    # PIL Image -> Numpy array (BGR formatına dönüştürme)
    image_np = np.array(image)
    if image_np.shape[-1] == 4:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
    elif image.mode == "RGB":
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)

    # Kırmızı renk aralıkları (iki ayrı aralık: düşük ve yüksek)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Kırmızı bölgeleri maskele
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Maske'yi invert et (yazı = beyaz, arka plan = siyah)
    inverted_mask = cv2.bitwise_not(red_mask)

    # Morfolojik açma-kapama ile küçük gürültüleri temizleyebilirsiniz (opsiyonel)
    kernel = np.ones((2,2), np.uint8)
    clean_mask = cv2.morphologyEx(inverted_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    clean_mask = cv2.morphologyEx(clean_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

    return clean_mask

def perform_ocr(processed_image):
    """
    Tesseract OCR işlemi.
    """
    custom_config = r'--oem 1 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config, lang='tur')
    return text

# Colab'da dosya yükleme butonu
uploaded = files.upload()

for filename in uploaded.keys():
    print("Yüklenen dosya:", filename)

    # Dosyayı PIL ile aç
    image_data = uploaded[filename]
    image = Image.open(io.BytesIO(image_data))

    # Orijinal görüntüyü göster
    plt.figure(figsize=(10,6))
    plt.imshow(image)
    plt.title("Orijinal Görüntü")
    plt.axis("off")
    plt.show()

    # Kırmızı arka planı maskele
    processed_mask = remove_red_background(image)

    # Ortaya çıkan maske'yi göster
    plt.figure(figsize=(10,6))
    plt.imshow(processed_mask, cmap='gray')
    plt.title("Renk Maskesi (Invert Edilmiş)")
    plt.axis("off")
    plt.show()

    # OCR uygula
    ocr_result = perform_ocr(processed_mask)
    print("OCR Sonucu:\n", ocr_result)
