from django import forms

from folders.models import Folder, UploadZip


class FolderCreationForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = [
            'name',
            'description',
            'price'
        ]
    name = forms.CharField(
        max_length=255,
        required=True,  # This makes the field required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Folder Name',
            'style': 'color: rgba(107, 0, 194, 0.726);'
        })
    )
    
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Price',
            'style': 'color: rgba(107, 0, 194, 0.726);'
        })
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Folder Description(optional)'
        }),
        required=False  # This makes the field optional
    )
    
    

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
            'class': 'form-control',  # Add your custom class here
            'style': 'margin-bottom: 1rem;',  # Add any inline styles here
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class UploadFileForm(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control form-select fw-bold',  # Add your custom class here
            'style': 'margin-bottom: 1rem;',  # Add any inline styles here
        })
    )
    images = MultipleFileField(
        required=True,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',  # Add your custom class here
            'style': 'margin-bottom: 1rem;',  # Add any inline styles here
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].choices = [('', 'Select a folder')] + list(self.fields['folder'].choices)
        
        
class UploadZipForm(forms.ModelForm):
    class Meta:
        model = UploadZip
        fields = ['folder', 'zip_file']
        widgets = {
            'folder': forms.Select(attrs={
                'class': 'form-control fw-bold', 
                'style': 'margin-bottom: 1rem;',
                'placeholder': 'Select a folder'
            }),
            'zip_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'zip_file': 'Choose Zip File',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['folder'].choices = [('', 'Select a folder')] + list(self.fields['folder'].choices)