from pdf2image import convert_from_path
import pytesseract
import util

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailsParser

poppler_path = r'C:\poppler-24.08.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract(file_path, file_format):
    # Step 1: Extracting text from the PDF file
    pages = convert_from_path(file_path, poppler_path=poppler_path)
    document_text = ''

    if len(pages) > 0:
        page = pages[0]
        processed_image = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text = '\n' + text

    # Step 2: Extract fields from the text
    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid document format: {file_format}")

    return extracted_data

if __name__ == '__main__':
    data = extract( r'C:\projects\medical_data_extraction\backend\resources\prescription/pre_2.pdf', 'prescription')
    print(data)
