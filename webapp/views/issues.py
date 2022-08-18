from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
# Create your views here.
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import IssueForm, SearchForm
from webapp.models import Issue, Project


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


class CreateIssue(PermissionRequiredMixin, CreateView):
    form_class = IssueForm
    template_name = "issues/create.html"

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("webapp:ProjectView", kwargs={"pk": self.object.project.pk})

    def has_permission(self):
        return self.request.user.has_perm("webapp.create_issue") or \
               self.request.user == self.get_object().users


class UpdateIssue(PermissionRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    context_object_name = 'issue'
    template_name = 'issues/update.html'
    permission_required = "webapp.update_issue"

    def get_success_url(self):
        return reverse('webapp:IssueView', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return self.request.user.has_perm("webapp.update_issue") or \
               self.request.user == self.get_object().users


class DeleteIssue(PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = 'issues/delete.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('webapp:IndexIssueView')
    permission_required = "webapp.update_issue"

    def has_permission(self):
        return self.request.user.has_perm("webapp.delete_issue") or \
               self.request.user == self.get_object().users
