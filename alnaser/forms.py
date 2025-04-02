from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from alnaser.models import Customer, Product, Category


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	
	phone = forms.CharField(label = "", max_length=15, widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder':'Phone Number'}), help_text='<span class="form-text text-muted"> <small>Enter your phone number, must be unique to your account.</small></span>')
	
	address = forms.CharField(label="",widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Your Address','rows': 3 }) ) 

            

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before.</small></span>'

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if Customer.objects.filter(phone=phone).exists():
			raise forms.ValidationError("This phone number is already registered.")
		return phone
	def save(self, commit=True):
		user = super().save(commit=False)
		if commit:
			user.save()
			Customer.objects.create(user = user, phone = self.cleaned_data['phone'], address = self.cleaned_data['address'])
		return user
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("This email address is already in use.")
		return email
	

class ProductAddForm(forms.ModelForm):
    ON_SALE_CHOICES = [
        (False, 'No'),
        (True, 'Yes'),
    ]
    on_sale = forms.ChoiceField(
        choices=ON_SALE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Product
        fields = ['name', 'price','barcode', 'description', 'image', 'category', 'on_sale', 'sale_price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].required = False  # Make image optional