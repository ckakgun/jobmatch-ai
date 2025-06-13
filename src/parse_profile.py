import pymupdf # to extract text from a pdf
import os


path = 'data/ceren_linkedin_profile.pdf'
def extract_text_from_pdf(path):
    'Extract linkedin profile text from a pdf file'
    doc = pymupdf.open(path)
    text =''
    for page in range(doc.page_count):
        text += doc.load_page(page).get_text()
    return text

if __name__ == "__main__":
    text = extract_text_from_pdf(path)
    print(text)
