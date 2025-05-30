import fitz  # PyMuPDF
import re

class ExtractCV:
        def __init__(self, pdf_path):
                self.pdf_path = pdf_path
                self.raw_text = ""
                self.cleaned_text = ""
        
        def get_raw_text(self):
                # Return the raw text extracted from the PDF
                if not self.raw_text:
                        self.extract_all_text()
                return self.raw_text
        
        def get_cleaned_text(self):
                # Return the cleaned text as a continuous string
                if not self.cleaned_text:
                        self.to_continuous_string()
                return self.cleaned_text

        def get_pdf_path(self):
                # Return the path to the PDF file
                return self.pdf_path

        def set_pdf_path(self, new_path):
                # Set a new path for the PDF file
                self.pdf_path = new_path
                self.raw_text = ""
                self.cleaned_text = ""

        def extract_all_text(self):
                # Extract all text from all pages of a PDF
                doc = fitz.open(self.pdf_path)
                full_text = ""
                for page in doc:
                        full_text += page.get_text()
                self.raw_text = full_text

        def to_continuous_string(self):
                # Convert text to a single continuous long string
                if not self.raw_text:
                        self.extract_all_text()
                cleaned = re.sub(r'\s+', ' ', self.raw_text)
                self.cleaned_text = cleaned.strip()
        
        def extract(self):
                # Convert the PDF to a continuous string
                self.extract_all_text()
                self.to_continuous_string()
        


