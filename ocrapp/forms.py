from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(required=False, label="Upload PDF")
    image_file = forms.ImageField(required=False, label="Upload Image")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("pdf_file") and not cleaned_data.get("image_file"):
            raise forms.ValidationError("Please upload a PDF or Image.")
