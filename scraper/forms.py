from django import forms

class ScraperForm(forms.Form):
    keyword = forms.CharField(
        label="Palabra clave",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Enviar resultados a este correo",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
