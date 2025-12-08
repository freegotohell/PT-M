import os
import PyPDF2
import re

from docx import Document


class DocumentProcessor:
    """
    A class for processing documents (DOCX and PDF) to extract dates following a specific target phrase.

    Attributes:
        target_phrase (str): The target phrase to search for in documents
        date_patterns (list): List of regex patterns for matching different date formats
    """
    def __init__(self):
        """Initialize the DocumentProcessor with target phrase and date patterns."""
        self.target_phrase = "Сроки оказания услуг по настоящему договору"
        self.date_patterns = [
            r'\b(\d{1,2}\.\d{1,2}\.\d{4})\b',  # dd.mm.yyyy
            r'\b(\d{1,2}\.\d{1,2}\.\d{2})\b',  # dd.mm.yy
            r'\b(\d{4}-\d{1,2}-\d{1,2})\b',  # yy.mm.dd
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # dd/mm/yyyy
            r'\b(\d{1,2}/\d{1,2}/\d{2})\b',  # dd/mm/yy
            r'(?:с\s+)(\d{1,2}\.\d{1,2}\.\d{4})(?:\s+по\s+)(\d{1,2}\.\d{1,2}\.\d{4})',
            r'(?:до\s+)(\d{1,2}\.\d{1,2}\.\d{4})',
            r'(?:по\s+)(\d{1,2}\.\d{1,2}\.\d{4})'
        ]

    def find_dates(self, text):
        """
        Find dates in the text that appear after the target phrase.

        Args:
            text (str): The text content to search through

        Returns:
            list: A list of unique date strings found after the target phrase,
                  or empty list if no dates found or target phrase not present
        """
        if not text:
            return []

        phrase_pos = text.find(self.target_phrase)
        if phrase_pos == -1:
            return []

        text_after_phrase = text[phrase_pos + len(self.target_phrase):phrase_pos + len(self.target_phrase) + 1000]
        dates = []

        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text_after_phrase, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    dates.extend([match.group(1), match.group(2)])
                else:
                    dates.append(match.group(1))

        return list(set(dates))

    def process_file(self, file_path):
        """
        Process a document file to extract dates following the target phrase.

        Args:
            file_path (str): Path to the document file to process
        """
        if file_path.lower().endswith('.docx'):
            text = self.docx_handler(file_path)
        elif file_path.lower().endswith('.pdf'):
            text = self.pdf_handler(file_path)
        else:
            print(f"Неподдерживаемый формат файла")
            return

        if not text:
            print("Не удалось извлечь текст")
            return

        if self.target_phrase not in text:
            print(f"Фраза '{self.target_phrase}' не найдена в документе")
            return

        dates = self.find_dates(text)

        if dates:
            for date in dates:
                print(f"{date}")
        else:
            print(f"Даты после фразы '{self.target_phrase}' не найдены")

    def docx_handler(self, file_path):
        """
       Extract text from a DOCX document file.

       Args:
           file_path (str): Path to the DOCX file

       Returns:
           str: Extracted text content from the document, or empty string on error
       """
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Ошибка при чтении DOCX файла {file_path}: {e}")
            return ""

    def pdf_handler(self, file_path):
        """
        Extract text from a PDF document file.

        Args:
            file_path (str): Path to the PDF file

        Returns:
            str: Extracted text content from the document, or empty string on error
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Ошибка при чтении PDF файла {file_path}: {e}")
            return ""


def main():
    processor = DocumentProcessor()
    file_path = input("Введите путь к файлу: ").strip()
    if os.path.exists(file_path):
        processor.process_file(file_path)
    else:
        print("Файл не найден")


if __name__ == "__main__":
    main()
