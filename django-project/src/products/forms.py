from django import forms

from .models import Product

# MODEL FORM


class Productform(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={"placeholder": "Your Title"}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"placeholder": "Your description", "class": "new-class-name two", "id": "my-id-for-textarea", "rows": 20, 'cols': 120}))
    price = forms.DecimalField(initial=199.9)
    email = forms.EmailField()

    class Meta:
        model = Product
        fields = {
            'title',
            'description',
            'price'
        }

    # # form validation
    # def clean_title(self):
    #     title = self.cleaned_data.get("title")
    #     if not "abd" in title:
    #         raise forms.ValidationError("This is not a valid title")
    #     else:
    #         return title

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not email.endswith("edu"):
    #         raise forms.ValidationError("This is not a valid email")
    #     else:
    #         return email


# Pure django form with widgets

class PureProductForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={"placeholder": "Your Title"}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={"placeholder": "Your description", "class": "new-class-name two", "id": "my-id-for-textarea", "rows": 20, 'cols': 120}))
    price = forms.DecimalField(initial=199.9)
