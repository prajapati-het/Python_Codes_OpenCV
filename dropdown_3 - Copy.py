import cv2
import os
import datetime
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.selected_filter = 'Original'
        self.capture_folder = None  # Path to the folder where captured images will be stored

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Filter Selection')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)

        self.filter_dropdown = QComboBox(self)
        self.filter_dropdown.addItems(['Original', 'Gray', 'Blur', 'Canny', 'Invert'])
        self.filter_dropdown.currentIndexChanged.connect(self.on_filter_change)
        self.layout.addWidget(self.filter_dropdown)

        self.choose_folder_button = QPushButton('Choose Folder', self)
        self.choose_folder_button.clicked.connect(self.choose_capture_folder)
        self.layout.addWidget(self.choose_folder_button)

        self.capture_button = QPushButton('Capture Photo', self)
        self.capture_button.clicked.connect(self.capture_photo)
        self.layout.addWidget(self.capture_button)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.show()

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            filtered_frame = self.apply_filter(frame, self.selected_filter)

            if len(filtered_frame.shape) == 3:
                h, w, ch = filtered_frame.shape
                bytes_per_line = ch * w
                q_img = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
                img = QImage(q_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            else:
                h, w = filtered_frame.shape
                bytes_per_line = w
                q_img = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2RGB)
                img = QImage(q_img.data, w, h, bytes_per_line * 3, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(img)
            self.video_label.setPixmap(pixmap)
            self.video_label.setScaledContents(True)

    def apply_filter(self, frame, selected_filter):
        if selected_filter == 'Original':
            return frame
        elif selected_filter == 'Gray':
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif selected_filter == 'Blur':
            return cv2.GaussianBlur(frame, (15, 15), 0)
        elif selected_filter == 'Canny':
            return cv2.Canny(frame, 100, 200)
        elif selected_filter == 'Invert':
            return cv2.bitwise_not(frame)
        else:
            return frame

    def on_filter_change(self, index):
        self.selected_filter = self.filter_dropdown.itemText(index)

    def choose_capture_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Capture Folder", "", options=options)
        if folder_path:
            self.capture_folder = folder_path
            print(f'Capture folder set to: {folder_path}')

    def capture_photo(self):
        if self.capture_folder is None:
            self.choose_capture_folder()

        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = os.path.join(self.capture_folder, f'captured_photo_{timestamp}.png')
            cv2.imwrite(filename, frame)
            print(f'Photo captured and saved as {filename}')

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication([])
    window = VideoApp()
    app.exec_()
