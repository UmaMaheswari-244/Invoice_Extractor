from flask import Flask, request, jsonify, render_template
import pdfplumber
from PIL import Image
import pytesseract
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="your api key")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Specify the full path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return str(e)

def generate_response(text):
    input_text = text + " Extract the customer details, product details only show the item and hsn/sac code and total amount from this invoice. "
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(input_text)
    clean_response = response.text.replace("*", "").strip()
    return clean_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'response': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'response': 'No selected file'}), 400

    if file:
        file_path = f"temp_{file.filename}"
        file.save(file_path)

        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(file_path)
        else:
            return jsonify({'response': 'Unsupported file type'}), 400

        response_text = generate_response(text)
        return jsonify({'response': response_text})

    return jsonify({'response': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
