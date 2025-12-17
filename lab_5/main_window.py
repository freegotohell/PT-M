import logging
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from iterator import Iterator

logger = logging.getLogger(__name__)


class Window(QMainWindow):
    def __init__(self):
        """
        creates a window for displaying images, with a button for switching
        between images and a button for selecting an annotation
        """
        super().__init__()
        logger.info("Main window initialized")

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
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "choose annotation",
            "",
            "CSV Files (*.csv)"
        )
        if not file_path:
            logger.info("Annotation file selection canceled by user")
            return

        logger.info("User selected annotation file: %s", file_path)

        try:
            self.iterator = Iterator(file_path)
            next(self.iterator)
            logger.info("Iterator initialized successfully")
            self.show_image()
            self.next.setEnabled(True)
            self.annotation.setEnabled(False)
        except StopIteration:
            logger.warning("Annotation file is empty: %s", file_path)
            self.image.setText("annotation is empty")
        except Exception as e:
            logger.exception(
                "Error %s while initializing iterator for file: %s",
                e,
                file_path
            )
            self.image.setText("error while reading annotation")

    def show_image(self) -> None:
        """
        shows the current image
        """
        if self.iterator is None:
            logger.warning("show_image called but iterator is None")
            self.image.setText("no annotation selected")
            return

        try:
            image_path = next(self.iterator)
            logger.info("Showing image: %s", image_path)
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                logger.error("Cannot load image: %s", image_path)
                self.image.setText(f"cant load: {image_path}")
            else:
                self.image.setPixmap(
                    pixmap.scaled(
                        self.image.size(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
        except StopIteration:
            logger.info("No more images to show (StopIteration)")
            self.next.setEnabled(False)
            self.image.setText("the end")
        except Exception as e:
            logger.exception("Unexpected error while showing image %s", e)
            self.image.setText("error while showing image")

    def show_next_image(self) -> None:
        """
        if it does not go beyond image_paths it increases the index value by 1
        and calls the function again
        """
        logger.debug("Next button clicked")
        self.show_image()
