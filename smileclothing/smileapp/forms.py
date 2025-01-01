from django import forms
from .models import Product
from .models import Profile,Order
from .models import ContactMessage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'slug', 'available', 'stock']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone_number', 'date_of_birth', 'profile_picture']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}),
        }



class AddressForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea, required=True)
    city = forms.CharField(max_length=100, required=True)
    zip_code = forms.CharField(max_length=6, required=True)



class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'city', 'zip_code', 'payment_method'] 