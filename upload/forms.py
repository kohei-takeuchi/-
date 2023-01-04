from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
class UploadFileForm(forms.Form):
    file = forms.FileField()
class devicedata(forms.Form):
    device = forms.fields.ChoiceField(
        choices = (
            ('deeper', 'Deeper'),
            ('sonar', 'ソナー'),
            ('multisonar', 'マルチビームソナー'),
            ('other', 'その他'),
        ),
        required=True,
    )
    depth = forms.FloatField(
    min_value=0)
