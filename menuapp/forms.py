from django import forms
from .models import Hotel, ManualCategory,MenuItem,Category

class HotelForm(forms.ModelForm):
    """
    Form for manually adding or editing hotels.
    Supports uploading logo and prevents duplicate hotel names.
    """

    class Meta:
        model = Hotel
        fields = ['name', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Hotel Name'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_name(self):
        """Ensure hotel name is unique (case-insensitive)."""
        name = self.cleaned_data['name'].strip()
        if Hotel.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A hotel with this name already exists.")
        return name
    
    



class MenuItemForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label="Upload Image")

    class Meta:
        model = MenuItem
        fields = [
            'item_name',
            'price',
            'categories',          # ✅ Auto Category
            'manual_categories',   # ✅ Manual Category
            'description',
            'image_url',
            'image_upload',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price (KD)'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'manual_categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Paste image URL or leave empty...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.order_by('name')
        self.fields['manual_categories'].queryset = ManualCategory.objects.order_by('name')
        self.fields['categories'].label = "Auto Category (Excel-linked)"
        self.fields['manual_categories'].label = "Manual Category (App-only)"