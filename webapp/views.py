from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import IssueForm
from webapp.models import Issue


class IndexView(TemplateView):
    def get(self, request):
        issues = Issue.objects.all()
        return render(request, 'index.html', {'issues': issues})


class IssueView(TemplateView):
    template_name = 'issue_view.html'

    def get_context_data(self,  **kwargs):
        kwargs['issue'] = get_object_or_404(Issue, pk=kwargs['pk'])
        return super().get_context_data(**kwargs)


class CreateIssue(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get("summary")
            description = form.cleaned_data.get("description")
            status = form.cleaned_data.get("status")
            type = form.cleaned_data.get("type")
            new_issue = Issue.objects.create(summary=summary, description=description, status=status, type=type)
            return redirect("IssueView", pk=new_issue.pk)
        return render(request, "create.html", {"form": form})


class UpdateIssue(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        issue = get_object_or_404(Issue, pk=pk)
        form = IssueForm(initial={
            "summary": issue.summary,
            "description": issue.description,
            "status": issue.status,
            "type": issue.type,
        })
        return render(request, 'update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        issue = get_object_or_404(Issue, pk=pk)
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue.summary = form.cleaned_data.get("summary")
            issue.description = form.cleaned_data.get("description")
            issue.status = form.cleaned_data.get("status")
            issue.type = form.cleaned_data.get("type")
            issue.save()
            return redirect('index')
        return render(request, 'update.html', {"form": form})


class DeleteIssue(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        issue = get_object_or_404(Issue, pk=pk)
        return render(request, 'delete.html', {'issue': issue})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        issue = get_object_or_404(Issue, pk=pk)
        issue.delete()
        return redirect('index')
