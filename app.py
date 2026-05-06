import sys
import cv2
import pytesseract
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

# 🔴 IMPORTANT: Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# ================= MAIN WINDOW =================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Vision Pro")
        self.setGeometry(300, 120, 700, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
            }
            QPushButton {
                background-color: #2563eb;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("AI Vision Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        subtitle = QLabel("Face Detection & Smart Text Recognition")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #94a3b8;")

        btn_face = QPushButton(" Face Detection")
        btn_text = QPushButton(" Text Recognition")

        btn_face.clicked.connect(self.open_face)
        btn_text.clicked.connect(self.open_text)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(40)
        layout.addWidget(btn_face)
        layout.addWidget(btn_text)

        self.setLayout(layout)

    def open_face(self):
        self.f = FaceWindow()
        self.f.show()

    def open_text(self):
        self.t = TextWindow()
        self.t.show()


# ================= FACE WINDOW =================
class FaceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection")
        self.setGeometry(300, 120, 700, 500)

        layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setStyleSheet("border: 2px dashed #334155;")

        self.result = QLabel("Faces Detected: 0")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setStyleSheet("font-size: 20px; font-weight: bold;")

        btn_upload = QPushButton(" Upload Image")
        btn_camera = QPushButton(" Open Camera")

        btn_upload.clicked.connect(self.upload)
        btn_camera.clicked.connect(self.camera)

        layout.addWidget(self.image_label)
        layout.addWidget(self.result)
        layout.addWidget(btn_upload)
        layout.addWidget(btn_camera)

        self.setLayout(layout)

    def display(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch*w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    def upload(self):
        file, _ = QFileDialog.getOpenFileName()
        if file:
            img = cv2.imread(file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Draw rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            self.result.setText(f"Faces Detected: {len(faces)}")
            self.display(img)

    def camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Draw rectangles
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

            cv2.putText(frame, f"Faces: {len(faces)}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Press Q to exit", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


# ================= TEXT WINDOW =================
class TextWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Recognition")
        self.setGeometry(300, 120, 700, 500)

        layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setStyleSheet("border: 2px dashed #334155;")

        self.result = QLabel("Recognized Text")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setStyleSheet("font-size: 20px; font-weight: bold;")

        btn_upload = QPushButton(" Upload Image")
        btn_camera = QPushButton(" Open Camera")

        btn_upload.clicked.connect(self.upload)
        btn_camera.clicked.connect(self.camera)

        layout.addWidget(self.image_label)
        layout.addWidget(self.result)
        layout.addWidget(btn_upload)
        layout.addWidget(btn_camera)

        self.setLayout(layout)

    def display(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch*w, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img))

    def recognize_text(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Improve quality
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        # Convert to black & white
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        return text.strip()

    def upload(self):
        file, _ = QFileDialog.getOpenFileName()
        if file:
            img = cv2.imread(file)
            text = self.recognize_text(img)
            self.result.setText("Text: " + text)
            self.display(img)

    def camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("Press C to capture", frame)

            key = cv2.waitKey(1)
            if key == ord('c'):
                text = self.recognize_text(frame)
                self.result.setText("Text: " + text)
                break
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


# ================= RUN =================
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())