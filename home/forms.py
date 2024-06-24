from django import forms
from .models import Communications, todo

class CommunicatonsForm(forms.ModelForm):
    class Meta:
        model = Communications
        fields  = '__all__'
        widgets = {
            'created_on': forms.DateInput(attrs={'type': 'date'}),
        }
        

class TodoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields = '__all__'
        widgets = {
            'added_on': forms.DateInput(attrs={'type': 'date'}),
        }


class UploadFileForm(forms.Form):
    file = forms.FileField()

class SelectContractors(forms.Form):
    contractor = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple)          