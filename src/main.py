import pathlib

import PyPDF2

from database import LiteDatabase
from extract_text import extract_text_from_word, extract_text_from_pdf, extract_text_from_powerpoint
from process_words import remove_stop_words
from collections import Counter


class Main:

    def __init__(self):

        self.repo_path = '/Users/jazib/Desktop/workrepo/FAST-Resources/'
        self.fast_resources = pathlib.Path(self.repo_path)
        self.db = LiteDatabase()

    def run(self):
        for file_path in self.fast_resources.rglob("*"):
            text = self.extract_text_from_file(file_path)
            if text is None:
                continue
            topic_name = self.extract_topic_name(str(file_path))
            filtered_words = remove_stop_words(text)

            url = self.create_absolute_link(file_path)
            self.db.insert_index(topic_name, url, Counter(filtered_words))
            print(file_path)

    def create_absolute_link(self, file_path):
        url = f"https://github.com/hassanzhd/FAST-Resources/blob/master/"
        url += str(file_path).replace(self.repo_path, "")
        url = url[:len(url)].replace(' ', '%20')
        return url

    def extract_text_from_file(self, file_path):
        if str(file_path).endswith(".pdf"):
            try:
                return extract_text_from_pdf(file_path)
            except (PyPDF2.utils.PdfReadError, ValueError) as e:
                print(f"Skipped non-PDF file: {file_path} ({str(e)})")

        elif str(file_path).endswith(".docx"):
            try:
                return extract_text_from_word(file_path)
            except Exception as e:
                print(f"Skipped non-Word file: {file_path} ({str(e)})")
        elif str(file_path).endswith(".pptx"):
            try:
                return extract_text_from_powerpoint(file_path)
            except Exception as e:
                print(f"Skipped non-PowerPoint file: {file_path} ({str(e)})")
        else:
            print(f"file not supported {file_path}")
            return None

    def extract_topic_name(self, file_path):
        file_path = file_path.replace(self.repo_path, "")
        endpoint = file_path.find('/')
        return file_path[:endpoint]


Main().run()
