from django import forms

class userForm(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    contraseña = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


class loginForm(forms.Form):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Apellido'}))
    email = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    contraseña = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class testUser(forms.Form):
    titulo = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de la imagen'}))
    archivo = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Seleccione un archivo'}))