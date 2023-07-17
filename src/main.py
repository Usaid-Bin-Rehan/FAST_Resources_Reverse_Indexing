import pathlib

import PyPDF2

from extract_text import extract_text_from_word, extract_text_from_pdf, extract_text_from_powerpoint
from process_words import remove_stop_words


class Main:

    def __init__(self):

        self.reverse_index = {}
        self.repo_path = '/Users/jazib/Desktop/workrepo/FAST-Resources/'
        self.fast_resources = pathlib.Path(self.repo_path)

    def run(self):
        for file_path in self.fast_resources.rglob("*"):
            text = self.extract_text_from_file(file_path)
            if text is None:
                continue
            filtered_text = remove_stop_words(text)
            topic_name = self.extract_topic_name(str(file_path))
            self.add_to_reverse_index(filtered_text, str(file_path))

    def add_to_reverse_index(self, filtered_text, file_path):
        for word in filtered_text:
            if word in self.reverse_index:
                self.reverse_index[word].add(file_path)
            else:
                self.reverse_index[word] = {file_path}

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
            print(f"file not supported ${file_path}")
            return None

    def extract_topic_name(self, file_path):
        file_path = file_path.replace(self.repo_path, "")
        endpoint = file_path.find('/')
        return file_path[:endpoint]


Main().run()
