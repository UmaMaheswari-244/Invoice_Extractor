import pdfplumber

# Function to extract text from a PDF
def extract_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

# Specify the path to the PDF file
pdf_path = r'C:\Users\USER\Desktop\LLM Intern\Sample Invoice.pdf'  # Replace with the actual path to your PDF file

# Extract and print the contents of the PDF
pdf_content = extract_pdf_text(pdf_path)
print(pdf_content)