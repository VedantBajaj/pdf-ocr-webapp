from django.shortcuts import render
from .forms import PDFUploadForm
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import platform

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def upload_pdf_or_image(request):
    text_output = ""
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data.get('pdf_file')
            image_file = form.cleaned_data.get('image_file')

            # Process PDF if uploaded
            if pdf_file:
                try:
                    images = convert_from_bytes(pdf_file.read())
                    for img in images:
                        img = img.resize((img.width // 2, img.height // 2))
                        text_output += pytesseract.image_to_string(img)
                        text_output += "\n\n--- End of Page ---\n\n"
                except Exception as e:
                    text_output = f"Error processing PDF: {e}"

            # Process Image if uploaded
            elif image_file:
                try:
                    img = Image.open(image_file)
                    img = img.convert('RGB')
                    img = img.resize((img.width // 2, img.height // 2))
                    text_output = pytesseract.image_to_string(img)
                except Exception as e:
                    text_output = f"Error processing image: {e}"

    else:
        form = PDFUploadForm()

    return render(request, 'ocrapp/upload.html', {
        'form': form,
        'text_output': text_output
    })