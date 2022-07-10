# from django import forms
# from django.forms import widgets
#
# from webapp.models import Status, Type
#
#
# class IssueForm(forms.Form):
#     summary = forms.CharField(max_length=50, required=False, label='Summary')
#     description = forms.CharField(max_length=3000, required=True, label="Description",
#                                   widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
#     type = forms.ModelChoiceField(queryset=Type.objects.all(), label='Type')
#     status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status')
#


from django import forms

from webapp.models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.all())
    status = forms.ModelChoiceField(queryset=Status.objects.all())

    class Meta:
        model = Issue
        fields = '__all__'
