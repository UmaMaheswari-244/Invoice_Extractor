import tkinter as tk
from tkinter import scrolledtext, filedialog
import pdfplumber
from PIL import Image
import pytesseract
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="your api key")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
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
    # Adjust the prompt to specify the desired format
    input_text = text + " Extract the customer details, product details and total amount from this invoice."
    if not input_text:
        response_output.delete("1.0", tk.END)
        response_output.insert(tk.END, "No text to process.")
        return

    # Create a chat session
    chat_session = model.start_chat(
        history=[
        ]
    )

    # Send the message and get the response
    response = chat_session.send_message(input_text)

    # Process response to remove any stars or unwanted formatting
    clean_response = response.text.replace("*", "").strip()

    # Update the response in the separate area
    response_output.delete("1.0", tk.END)
    response_output.insert(tk.END, clean_response)

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("PNG files", "*.png")]
    )
    print(f"Selected file: {file_path}")  # Debugging line to check the selected file
    if file_path:
        if file_path.lower().endswith('.png'):
            text = extract_text_from_image(file_path)
        elif file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        else:
            response_output.delete("1.0", tk.END)
            response_output.insert(tk.END, "Unsupported file type.")
            return
        generate_response(text)

# Create the main window
root = tk.Tk()
root.title("Generative AI Chat")

# Create and place widgets
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

open_file_button = tk.Button(input_frame, text="Select PDF or PNG", command=open_file)
open_file_button.pack(pady=5)

# Separate area for response
response_frame = tk.Frame(root)
response_frame.pack(pady=10)

response_label = tk.Label(response_frame, text="Response:")
response_label.pack(anchor="w", padx=10)

response_output = scrolledtext.ScrolledText(response_frame, width=60, height=20, wrap=tk.WORD)
response_output.pack(padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
