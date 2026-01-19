from django import forms
from .models import Batch

class BulkEnrollForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all())
    start_date = forms.DateField(required=False, help_text="Leave blank to use today.")