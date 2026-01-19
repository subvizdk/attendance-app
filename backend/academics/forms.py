from django import forms

class StudentImportForm(forms.Form):
    file = forms.FileField(help_text="Upload .xlsx file")
