from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Issue, Project


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["summary", "description", "type", "status"]
        widgets = {
            "type": widgets.CheckboxSelectMultiple
        }

        def clean(self):
            if self.cleaned_data.get("summary") == self.cleaned_data.get("description"):
                raise ValidationError("Краткий заголовок и описание не могут совпадать")
            return super().clean()


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Поиск')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['p_name', 'p_description', 'start_date', 'expiration_date']
        widgets = {
            "p_description": widgets.Textarea(attrs={"placeholder": "Введите описание"})
        }

    def clean(self):
        if self.cleaned_data.get("p_name") == self.cleaned_data.get("p_description"):
            raise ValidationError("Название и описание проекта не могут совпадать")
        return super().clean()
