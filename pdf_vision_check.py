import fitz  # PyMuPDF
import easyocr
from PIL import Image
import io
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re
from fuzzywuzzy import fuzz
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json  # Add this import for working with JSON

# Initialize the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Function to correct text spacing using GPT-2
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

# Function to categorize PDF type based on content
def categorize_pdf(pdf_text):
    filtered_text = filter_non_english_words(pdf_text)
    corrected_text = correct_text_spacing(filtered_text)
    
    categories = {
    "School 10th Certificate": [
        "tenth", "ten", "class x", "school leaving", "secondary school", "ssc", 
        "matriculation", "10th grade", "10th standard", "grade 10", "standard 10"
    ],
    "School 12th Certificate": [
        "twelfth", "twelve", "class xii", "higher secondary", "hsc", "intermediate", 
        "senior secondary", "12th grade", "12th standard", "grade 12", "standard 12"
    ],
    "Internship Certificate": [
        "internship certificate", "intern", "certify", "internship completion", 
        "work experience", "internship program", "internship achievement"
    ],
    "Marksheet": [
        "marksheet", "result sheet", "grade report", "academic record", "transcript", 
        "scorecard", "grade sheet", "exam results", "report card"
    ],
    "Project Certificate": [
        "project certificate", "project completion", "project work", "project accomplishment", 
        "project achievement", "project participation"
    ],
    "Certification": [
        "certification", "certified", "credential", "qualification", "course completion", 
        "completion certificate", "professional certification", "training certification", 
        "skills certification"
    ],
    "Competition Certificate": [
        "competition certificate", "contest", "winner", "participation", "achievement", 
        "runner-up", "second position", "third position", "first place", "second place", 
        "third place", "finalist", "champion", "competition achievement", "contest winner","certify"
    ],
    "Course Certificate": [
        "course certificate", "course completion", "training", "learning certificate", 
        "educational certificate", "course achievement", "course participation"
    ]}

    max_score = 0
    best_match = "Unknown Type"
    
    for category, keywords in categories.items():
        for keyword in keywords:
            score = fuzz.partial_ratio(keyword.lower(), corrected_text.lower())
            if score > max_score:
                max_score = score
                best_match = category
    
    return best_match

# Function to download PDF from Google Drive
def download_pdf_from_drive(drive_url, credentials):
    file_id = drive_url.split('/')[-2]
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = io.BytesIO(fh)
    downloader.seek(0)
    downloader.truncate(0)
    downloader.write(request.execute())
    return fh

# Function to analyze PDF from Google Drive
def analyze_pdf_from_drive(drive_url, credentials):
    pdf_file = download_pdf_from_drive(drive_url, credentials)
    pdf_text = extract_text_from_pdf(pdf_file)
    pdf_type = categorize_pdf(pdf_text)
    return pdf_type

# Load Google Drive API credentials from JSON file
def load_drive_credentials(credentials_file):
    with open(credentials_file) as f:
        credentials_data = json.load(f)
    
    credentials = service_account.Credentials.from_service_account_info(
        credentials_data,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    
    return credentials

# Example usage
credentials_file = "client_secret_1085110021850-k8vej60tpobolqao0arknnrt3i5v68bh.apps.googleusercontent.com.json"  # Path to your updated credentials file

credentials = load_drive_credentials(credentials_file)
drive_service = build('drive', 'v3', credentials=credentials)
# Example usage
drive_url = "https://drive.google.com/file/d/1hvmAtqvR2L4WIa4OAlR2Av3rh8B2ksBY/view"

pdf_type = analyze_pdf_from_drive(drive_url, credentials)
print("PDF Type:", pdf_type)
