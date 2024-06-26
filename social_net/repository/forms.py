from django import forms
from django.db.models.functions import Lower

from .models import Repository


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class RepositoryCreationForm(forms.ModelForm):
    files = forms.FileField(widget=MultipleFileInput(attrs={
        'multiple': True,
        'webkitdirectory': True,
        'directory': True,
        'allow_empty': True,
    }), required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Repository
        fields = ['name', 'description', 'type', 'price']

    def clean_name(self):
        data = self.cleaned_data['name']
        if Repository.objects.filter(user=self.user).annotate(lower_name=Lower('name')).filter(lower_name=data.lower()).exists():
            raise forms.ValidationError('Repository with such name already exists.')
        return data
