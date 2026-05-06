# 🤖 AI Vision Pro

A modern AI-based desktop application for **Face Detection** and **Text Recognition** using Computer Vision.

---

## ✨ Features

### 👤 Face Detection

* Detects human faces in images and live camera feed
* Displays **number of faces detected**
* Draws **bounding boxes** around faces

### 📝 Text Recognition (OCR)

* Extracts text from images and camera input
* Supports **printed and clean handwritten text**
* Uses Tesseract OCR for accurate results

### 🎯 User Interface

* Modern dark-themed GUI
* Image upload + live camera support
* Clean and professional layout

---

## 🛠️ Technologies Used

* Python
* OpenCV
* PyQt5
* pytesseract
* Tesseract OCR

---

## 📦 Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/AI-Vision-Pro.git
cd AI-Vision-Pro
```

### 2. Install dependencies

```
pip install opencv-python pyqt5 pytesseract numpy
```

### 3. Install Tesseract OCR

Download and install Tesseract OCR, then update the path in `app.py`:

```
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## ▶️ How to Run

```
python app.py
```

---

## 📸 Usage

### Face Detection

* Click **Face Detection**
* Upload an image or use camera
* View face count with bounding boxes

### Text Recognition

* Click **Text Recognition**
* Upload an image or capture from camera
* Extract and display text

---

## ⚠️ Limitations

* Handwritten text recognition works best with:

  * Clear writing
  * Capital letters
  * Good lighting

* Complex cursive handwriting may not be detected accurately

---

## 🚀 Future Improvements

* Advanced handwritten text recognition using deep learning
* Better UI animations and transitions
* Export detected text to file
* Multi-language OCR support

---

## 👩‍💻 Author

Sara Bhure

---

## 📌 Note

This project is developed for educational purposes to demonstrate practical implementation of Computer Vision and OCR technologies.
