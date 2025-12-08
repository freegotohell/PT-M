import os
import re
import argparse
import PyPDF2

from docx import Document


class DocumentProcessor:
    """
    A class for processing documents (DOCX and PDF) to extract dates and cities
    following a specific target phrase.

    Attributes:
        target_phrase (str): The target phrase to search for in documents
        date_patterns (list): List of regex patterns for matching different date formats
        city_pattern (str): Regex pattern for matching city name like 'г. Самара'
    """
    def __init__(self):
        """Initialize the DocumentProcessor with target phrase, date and city patterns."""
        self.target_phrase = "Сроки"
        self.date_patterns = [
            r'\b(\d{1,2}\.\d{1,2}\.\d{4})\b',
            r'\b(\d{1,2}\.\d{1,2}\.\d{2})\b',
            r'\b(\d{4}-\d{1,2}-\d{1,2})\b',
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',
            r'\b(\d{1,2}/\d{1,2}/\d{2})\b',
            r'(?:с\s+)(\d{1,2}\.\d{1,2}\.\d{4})(?:\s+по\s+)(\d{1,2}\.\d{1,2}\.\d{4})',
            r'(?:до\s+)(\d{1,2}\.\d{1,2}\.\d{4})',
            r'(?:по\s+)(\d{1,2}\.\d{1,2}\.\d{4})'
        ]
        # Pattern for Russian city in format "г. Самара", "г. Москва", etc.
        self.city_pattern = r'(г\. [А-ЯЁ][а-яё]{2,}(?:[ -][А-ЯЁ][а-яё]{2,})*)\s{3,}'

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

        # Search only in a limited window after the target phrase
        text_after_phrase = text[phrase_pos + len(self.target_phrase):phrase_pos + len(self.target_phrase) + 1000]
        dates = []

        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text_after_phrase, re.IGNORECASE)
            for match in matches:
                # Handle "from ... to ..." date range
                if len(match.groups()) == 2:
                    dates.extend([match.group(1), match.group(2)])
                else:
                    dates.append(match.group(1))

        return list(set(dates))

    def find_cities(self, text):
        """
        Find city names in the text in format 'г. Самара'.

        Args:
            text (str): The text content to search through

        Returns:
            list: A list of unique city strings like 'г. Самара'
        """
        if not text:
            return []

        matches = re.finditer(self.city_pattern, text)
        cities = [m.group(1) for m in matches]
        return list(set(cities))

    def process_file(self, file_path, mode="date"):
        """
        Process a document file to extract dates and/or cities.

        Args:
            file_path (str): Path to the document file to process
            mode (str): What to search for: "date", "city", or "both"
        """
        if file_path.lower().endswith('.docx'):
            text = self.docx_handler(file_path)
        elif file_path.lower().endswith('.pdf'):
            text = self.pdf_handler(file_path)
        else:
            print("Unsupported file format")
            return

        if not text:
            print("Failed to extract text")
            return

        search_dates = mode in ("date", "both")
        search_cities = mode in ("city", "both")

        # If searching for dates, ensure target phrase exists
        if search_dates and self.target_phrase not in text:
            print(f"Phrase '{self.target_phrase}' not found in document")
            # Still may want to search for cities even if phrase not found
            if not search_cities:
                return

        dates = []
        cities = []

        if search_dates:
            dates = self.find_dates(text)

        if search_cities:
            cities = self.find_cities(text)

        if search_dates:
            if dates:
                print("Dates:")
                for date in dates:
                    print(date)
            else:
                print(f"No dates found after phrase '{self.target_phrase}'")

        if search_cities:
            if cities:
                print("Cities:")
                for city in cities:
                    print(city)
            else:
                print("No cities found in format 'г. <City>'")

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
            print(f"Error reading DOCX file {file_path}: {e}")
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
            print(f"Error reading PDF file {file_path}: {e}")
            return ""


def parse_args():
    """
    Parse command-line arguments.

    Positional:
        file              Path to file

    Options:
        --mode {date,city,both}
                           What to search for (default: date)
    """
    parser = argparse.ArgumentParser(description="Process DOCX/PDF to extract dates and cities")
    parser.add_argument("file", help="Path to DOCX or PDF file")
    parser.add_argument(
        "--mode",
        choices=["date", "city", "both"],
        default="date",
        help="What to search for: 'date', 'city', or 'both' (default: date)"
    )
    return parser.parse_args()


def main():
    processor = DocumentProcessor()
    file_path = input("Введите путь к файлу: ").strip()
    mode = "both"

    if os.path.exists(file_path):
        processor.process_file(file_path, mode=mode)
    else:
        print("File not found")


if __name__ == "__main__":
    main()
