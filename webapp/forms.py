from django import forms

from webapp.models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.all())
    status = forms.ModelChoiceField(queryset=Status.objects.all())

    class Meta:
        model = Issue
        fields = '__all__'
