import pytesseract
from pdf2image import convert_from_bytes
from django.shortcuts import render
from .forms import PDFUploadForm
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def upload_pdf(request):
    text_output = ""
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            images = convert_from_bytes(pdf_file.read())
            for img in images:
                text_output += pytesseract.image_to_string(img)
    else:
        form = PDFUploadForm()
    return render(request, 'ocrapp/upload.html', {'form': form, 'text_output': text_output})