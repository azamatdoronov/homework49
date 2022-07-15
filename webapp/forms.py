from django import forms
from django.forms import widgets

from webapp.my_validate import special_words, special_chars, check_status, check_count
from webapp.models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    summary = forms.CharField(max_length=50, validators=(special_chars,))
    description = forms.CharField(max_length=3000, validators=(special_words,),
                                  widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), validators=(check_count,),
                                          widget=forms.CheckboxSelectMultiple)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), empty_label=None, validators=(check_status,))


    class Meta:
        model = Issue
        fields = '__all__'
