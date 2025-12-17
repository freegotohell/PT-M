from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from iterator import Iterator


class Window(QMainWindow):
    def __init__(self):
        """
        creates a window for displaying images, with a button for switching between images and a button for selecting an
        annotation
        """
        super().__init__()

        self.iterator = None

        self.setWindowTitle("sssnakes")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image = QLabel("here is a pic")
        self.image.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image)

        self.annotation = QPushButton("choose annotation")
        self.annotation.clicked.connect(self.select_annotation_file)
        self.layout.addWidget(self.annotation)

        self.next = QPushButton("next")
        self.next.setEnabled(False)
        self.next.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next)

    def select_annotation_file(self):
        """
        opens a file selection dialog box and processes the user's selection
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "choose annotation", "", "CSV Files (*.csv)")
        if file_path:
            self.iterator = Iterator(file_path)
            try:
                next(self.iterator)
                self.show_image()
                self.next.setEnabled(True)
                self.annotation.setEnabled(False)
            except StopIteration:
                self.image.setText("annotation is empty")

    def show_image(self) -> None:
        """
        shows the current image
        """
        try:
            image_path = next(self.iterator)
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.image.setText(f"cant load: {image_path}")
            else:
                self.image.setPixmap(pixmap.scaled(self.image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except StopIteration:
            self.next.setEnabled(False)
            self.image.setText("the end")

    def show_next_image(self) -> None:
        """
        if it does not go beyond image_paths it increases the index value by 1 and calls the function again
        """
        self.show_image()
