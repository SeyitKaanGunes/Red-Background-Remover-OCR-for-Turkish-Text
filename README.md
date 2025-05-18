# 🔍 Red Background Remover & OCR for Turkish Text

This project is a Google Colab-compatible image processing pipeline that:

✅ Removes red backgrounds from images  
✅ Extracts white-colored **Turkish** text  
✅ Uses Tesseract OCR to convert image content into readable text

---

## 📸 What It Does

When you upload an image with a **red background and white text**, the script:

1. Detects red areas using HSV color masking
2. Inverts the mask to isolate white text
3. Applies morphological operations to clean up noise
4. Runs **Tesseract OCR (Turkish language)** to extract the text

Works especially well for:
- Posters with red backgrounds
- Documents or visuals with strong red coloring
- White-on-red warning labels, graphics, or forms

---
## 🧠 How It Works – Core Functions

### 🔻 `remove_red_background(image)`

- Converts image to HSV color space
- Masks red areas using two HSV ranges
- Inverts the mask so text appears white
- Optionally applies morphological operations

### 🔠 `perform_ocr(processed_image)`

- Uses Tesseract with `--psm 6` layout mode
- Language set to `tur` (Turkish)
- Extracts text from the masked image

---
## 📦 Dependencies

- OpenCV
- NumPy
- Matplotlib
- Tesseract OCR
- Turkish OCR package: `tesseract-ocr-tur`

---

## 🔒 Notes

- Only red → white contrast is currently supported
- Works best with clean, high-contrast images
- Use `RGBA` or `RGB` compatible formats (e.g., .png, .jpg)
