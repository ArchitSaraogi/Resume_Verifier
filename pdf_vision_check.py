import fitz  # PyMuPDF
import easyocr
from PIL import Image
import io
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from fuzzywuzzy import fuzz

# Initialize the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def correct_text_spacing(text):
    input_ids = tokenizer.encode(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model.generate(input_ids, max_length=1024, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pdf_text += page.get_text("text") + "\n"
    return pdf_text

# Function to extract images from PDF using PyMuPDF and perform OCR using EasyOCR
def extract_text_from_images(pdf_path):
    reader = easyocr.Reader(['en'])  # Specify the language(s) for OCR
    doc = fitz.open(pdf_path)
    image_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)  # Convert PIL image to numpy array
            text = reader.readtext(image_np, detail=0)
            image_text += " ".join(text) + "\n"
    return image_text

# Function to filter non-English words
def filter_non_english_words(text):
    words = text.split()
    english_words = [word for word in words if word.isascii() and word.isalpha()]
    filtered_text = ' '.join(english_words)
    return filtered_text

# Function to categorize PDF type using fuzzy matching
def categorize_pdf(text):
    categories = {
        "School 10th Certificate": [
            "10th", "tenth", "ten", "class x", "class ten", "ssc", "secondary school certificate", 
            "school leaving certificate", "high school certificate", "matriculation"
        ],
        "School 12th Certificate": [
            "12th", "twelfth", "twelve", "class xii", "class twelve", "hsc", "higher secondary certificate", 
            "senior secondary certificate", "intermediate certificate", "pre-university certificate"
        ],
        "Internship Certificate": [
            "internship certificate", "internship", "intern", "certify", "internship completion certificate",
            "certificate of internship", "internship participation", "internship acknowledgment"
        ],
        "Marksheet": [
            "marksheet", "mark sheet", "result sheet", "grade report", "score sheet", "academic record",
            "transcript", "grade card", "statement of marks", "report card"
        ],
        "Project Certificate": [
            "project certificate", "project completion certificate", "certificate of project", 
            "project accomplishment", "project completion", "project report certificate"
        ],
        "Certification": [
            "certification", "certified", "credential", "certificate", "certified completion",
            "certificate of achievement", "professional certification", "certificate of qualification"
        ]
    }

    text_lower = text.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if fuzz.partial_ratio(text_lower, keyword.lower()) > 70:  # Using a threshold for fuzzy matching
                return category
    return "Unknown Type"

# Main function
def main(pdf_path):
    pdf_text = extract_text_from_pdf(pdf_path)
    image_text = extract_text_from_images(pdf_path)
    combined_text = pdf_text + "\n" + image_text
    filtered_text = filter_non_english_words(combined_text)
    corrected_text = correct_text_spacing(filtered_text)
    pdf_type = categorize_pdf(corrected_text)
    print("PDF Type:", pdf_type)

# Example usage
pdf_path = "C:\\Users\\i_sar\\OneDrive\\Desktop\\Resume_Authourizer\\Test_cases\\ashishnaik123.pdf"
main(pdf_path)