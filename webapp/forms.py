from django import forms
from django.forms import widgets

from webapp.models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True, label='Заголовок:')
    description = forms.CharField(max_length=3000, required=True, label='Описание:',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label='Тип:')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False, label='Статус:')

    class Meta:
        model = Issue
        fields = '__all__'
