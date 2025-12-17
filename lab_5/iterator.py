import logging

logger = logging.getLogger(__name__)


class Iterator:
    def __init__(self, annotation: str) -> None:
        self.annotation = annotation
        logger.info("Opening annotation file: %s", annotation)
        self.file = open(annotation, 'r', encoding='utf-8')
        next(self.file)
        logger.debug("Skipped header line in annotation")

    def __iter__(self) -> 'Iterator':
        return self

    def __next__(self) -> str:
        line = self.file.readline().strip()
        if line:
            logger.debug("Read line from annotation: %s", line)
            part = line.split(',')
            if not part:
                logger.warning("Empty split parts for line: %s", line)
            return part[0]
        else:
            logger.info("Reached end of annotation file")
            raise StopIteration