from django.shortcuts import render
from .forms import PDFUploadForm
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import platform

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def upload_pdf(request):
    text_output = None
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            images = convert_from_bytes(pdf_file.read(), first_page=1, last_page=1)  # Limit to 1 page
            text_output = ''
            for img in images:
                img = img.resize((img.width // 2, img.height // 2))  # Resize to reduce memory
                text_output += pytesseract.image_to_string(img)
    else:
        form = PDFUploadForm()
    return render(request, 'ocrapp/upload.html', {'form': form, 'text_output': text_output})