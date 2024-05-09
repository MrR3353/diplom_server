from django import forms
from .models import Repository


class RepositoryCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Repository
        fields = ['name', 'description']

    def clean_name(self):
        data = self.cleaned_data['name']
        if Repository.objects.filter(user=self.user, name=data).exists():
            raise forms.ValidationError('Repository with such name already exists.')
        return data
