import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text() if page.extract_text() else ""
    return text


print(extract_text_from_pdf('./papers/CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis.pdf'))