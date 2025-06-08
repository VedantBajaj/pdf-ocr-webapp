from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(required=False, label="Upload PDF")
    image_file = forms.ImageField(required=False, label="Upload Image")

    def clean(self):
        cleaned_data = super().clean()
        pdf = cleaned_data.get("pdf_file")
        image = cleaned_data.get("image_file")
        if not pdf and not image:
            raise forms.ValidationError("Please upload a PDF or an image.")
        return cleaned_data
