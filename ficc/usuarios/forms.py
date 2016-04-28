from django import forms
from django.contrib.auth.models import User

class EditForm(forms.ModelForm):
    password1 = forms.CharField(max_length=10, widget= forms.PasswordInput)
    password2 = forms.CharField(max_length=10, widget= forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required =True)
    last_name = forms.CharField(max_length=30, required =True)
    email = forms.EmailField(required =True)
    #nacionalidad = forms.ChoiceField(choices=COUNTRY_CHOICES)
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        num_words = len(password1)
        if num_words < 6:
            raise forms.ValidationError('Contrasenha debil')
        return password1	
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError('Repita la contrasenha correctamente')        
        return password2	
    #class Meta:
     #   model = User
      #  fields = ('first_name', 'last_name', 'email', 'nacionalidad',)

ASUNTO = (
    ('Desarrollador', 'Solicitar ser Desarrollador'),
    ('Mensaje Privado', 'Mensaje'),
    ('Compartir', 'Compartir'),
)

class MensajePvForm(forms.ModelForm):
    asunto = forms.ChoiceField(choices=ASUNTO)
    destinatario = forms.EmailField(initial = 'user7@example.com')
    cuerpo = forms.CharField(widget=forms.Textarea())
    pagina_web = forms.URLField(required=True)


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=10, widget= forms.PasswordInput)
    password2 = forms.CharField(max_length=10, widget= forms.PasswordInput)
    #nacionalidad = forms.ChoiceField(choices=COUNTRY_CHOICES)
    #first_name = forms.CharField(max_length=30, required = True )
    #last_name = forms.CharField(max_length=30, required = True )
    #email = forms.EmailField(max_length=75,required=True)
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        num_words = len(password1)
        if num_words < 6:
            raise forms.ValidationError('Password debil')
        return password1
		
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError('Repita el password correctamente')        
        return password2
	
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
    
