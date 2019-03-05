from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    sender = forms.EmailField(widget=forms.TextInput(attrs={'size':'40','class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    copy = forms.BooleanField(required=False)

class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Login'
		self.fields['password'].label = 'Parol'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('Bu loginle artig istifadeci muvcuddur!')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Parol yalnisdir!')

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
		]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Login'
		self.fields['password'].label = 'Parol'
		self.fields['password'].help_text = 'Parol Fikirlesin'
		self.fields['password_check'].label = 'Parolu tekrar edin'
		self.fields['first_name'].label = 'Ad'
		self.fields['last_name'].label = 'Familya'
		self.fields['email'].label = 'Email addresiniz'
		self.fields['email'].help_text = 'Xaish edirik real email qeyd edesiniz'


	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Bu loginle artig istifadeci muvcuddur!')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Bu email adresle artig istifadeci movcuddur!')
		if password != password_check:
			raise forms.ValidationError('Parollarin tekrarinda yalnish var . yeniden deneyin!')







class OrderForm(forms.Form):

	name = forms.CharField()
	last_name = forms.CharField(required=False)
	phone = forms.CharField()
	buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "Ozunuz yaxinlashacaqsiniz?"),("delivery", "Catdirilma")]))
	date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
	address = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = 'Ad'
		self.fields['last_name'].label = 'Familya'
		self.fields['phone'].label = 'Elaqe nomresi'
		self.fields['phone'].help_text = 'Xaish edirik ishlek telefon nomresi qeyd edin'
		self.fields['buying_type'].label = 'Mehsulu nece elde edecem?'
		self.fields['address'].label = 'Catdirilma addresi'
		self.fields['address'].help_text = '*Seheri mutleq qeyd edin!'
		self.fields['comments'].label = 'Sifarishle bagli comment'
		self.fields['date'].label = 'Catdirilma tarixi'
		self.fields['date'].help_text = 'Sifarish tesdiq olundugdan 1 gun sonra menegerler sizinle elaqe saxlayacaq!'
