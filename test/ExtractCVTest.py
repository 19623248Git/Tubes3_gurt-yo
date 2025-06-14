import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.ExtractCV import ExtractCV as ecv

if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
                print("Usage: python script.py <pdf_path>")
                sys.exit(1)

        pdf_path = sys.argv[1]
        cv = ecv(pdf_path)
        cv.extract()  # Extracts text from the PDF and converts it to a continuous string

        continuous_text = cv.get_cleaned_text()

        print("Extracted Continuous Text:\n")
        print(continuous_text)