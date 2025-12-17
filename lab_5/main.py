import sys
import logging

from PyQt5.QtWidgets import QApplication
from main_window import Window

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Application starting")
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        exit_code = app.exec()
        logger.info("Application finished with code %s", exit_code)
        sys.exit(exit_code)
    except Exception as e:  # global catch-all
        logger.exception("Unhandled exception in main %s", e)


if __name__ == '__main__':
    main()
