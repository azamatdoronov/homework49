from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import IssueForm, SearchForm
from webapp.models import Issue


class IndexIssueView(ListView):
    model = Issue
    template_name = "issues/index.html"
    context_object_name = "issues"
    ordering = "-updated_at"
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if self.search_value:
            return Issue.objects.filter(
                Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value))
        return Issue.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["form"] = self.form
        if self.search_value:
            query = urlencode({'search': self.search_value})
            context['query'] = query
            context['search'] = self.search_value
        return context

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class IssueView(DetailView):
    template_name = "issues/issue_view.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project.p_name
        return context


class CreateIssue(CreateView):
    form_class = IssueForm
    template_name = "issues/create.html"

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.save()
        form.save_m2m()
        return redirect("IssueView", pk=issue.pk)


class UpdateIssue(UpdateView):
    model = Issue
    form_class = IssueForm
    context_object_name = 'issue'
    template_name = 'issues/update.html'

    def get_success_url(self):
        return reverse('IssueView', kwargs={'pk': self.object.pk})


class DeleteIssue(DeleteView):
    model = Issue
    template_name = 'issues/delete.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('IndexIssueView')
