from django import forms
from .models import Task


class TaskCreationForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required= False)
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']


class TaskUpdateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', ]