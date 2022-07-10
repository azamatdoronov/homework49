from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import TemplateView, RedirectView

from webapp.forms import IssueForm
from webapp.models import Issue


class IndexView(View):
    def get(self, request, *args, **kwargs):
        issue = Issue.objects.order_by("-updated_at")
        context = {"issue": issue}
        return render(request, "index.html", context)


class MyRedirectView(RedirectView):
    url = "/"


class IssueView(TemplateView):
    template_name = "issue_view.html"

    # extra_context = {"test": "test"}
    # def get_template_names(self):
    #     return "article_view.html"

    def get_context_data(self, **kwargs):
        pk = kwargs.get("pk")
        issue = get_object_or_404(Issue, pk=pk)
        kwargs["issue"] = issue
        return super().get_context_data(**kwargs)


def create_issue(request):
    if request.method == "GET":
        form = IssueForm()
        return render(request, "create.html", {"form": form})
    else:
        form = IssueForm(data=request.POST)
        if form.is_valid():
            summary = form.cleaned_data.get("summary")
            description = form.cleaned_data.get("description")
            status = form.cleaned_data.get("status")
            type = form.cleaned_data.get("type")
            new_issue = Issue.objects.create(summary=summary, description=description, status=status, type=type)
            return redirect("issue_view", pk=new_issue.pk)
        return render(request, "create.html", {"form": form})


def update_issue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "GET":
        form = IssueForm(initial={
            "summary": issue.summary,
            "description": issue.description,
            "status": issue.status,
            "type": issue.type,
        })
        return render(request, "update.html", {"form": form})
    else:
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue.summary = form.cleaned_data.get("summary")
            issue.description = form.cleaned_data.get("description")
            issue.status = form.cleaned_data.get("status")
            issue.type = form.cleaned_data.get("type")
            issue.save()
            return redirect("issue_view", pk=issue.pk)
        return render(request, "update.html", {"form": form})


def delete_issue(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == "GET":
        pass
    #     return render(request, "delete.html", {"article": article})
    else:
        issue.delete()
        return redirect("index")
