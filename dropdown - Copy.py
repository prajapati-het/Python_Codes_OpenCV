import cv2
import datetime
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

class VideoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = cv2.VideoCapture(0)
        self.selected_filter = 'Original'

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

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication([])
    window = VideoApp()
    app.exec_()
