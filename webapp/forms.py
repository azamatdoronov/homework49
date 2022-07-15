from django import forms
from django.forms import widgets

from webapp.models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, required=True, label='Заголовок:')
    description = forms.CharField(max_length=3000, required=False, label='Описание:',
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), required=True, label='Тип:')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label=None, required=True, label='Статус:')

    class Meta:
        model = Issue
        fields = '__all__'
