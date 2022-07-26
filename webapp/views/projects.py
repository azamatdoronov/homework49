# from django.db.models import Q
# from django.shortcuts import render, redirect, get_object_or_404
# # Create your views here.
# from django.urls import reverse
# from django.utils.http import urlencode
# from django.views import View
# from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView
#
# from webapp.views.base_view import FormView as CustomFormView
# from webapp.forms import IssueForm, SearchForm, ProjectForm
# from webapp.models import Issue, Project
#
#
# class IndexView(ListView):
#     model = Project
#     template_name = "projects/index.html"
#     context_object_name = "projects"
#     ordering = "-updated_at"
#     paginate_by = 2
#
#     def get(self, request, *args, **kwargs):
#         self.form = self.get_search_form()
#         self.search_value = self.get_search_value()
#         return super().get(request, *args, **kwargs)
#
#     def get_queryset(self):
#         if self.search_value:
#             return Project.objects.filter(
#                 Q(p_description__icontains=self.search_value) | Q(p_name__icontains=self.search_value))
#         return Project.objects.all()
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=object_list, **kwargs)
#         context["form"] = self.form
#         if self.search_value:
#             query = urlencode({'search': self.search_value})
#             context['query'] = query
#             context['search'] = self.search_value
#         return context
#
#     def get_search_form(self):
#         return SearchForm(self.request.GET)
#
#     def get_search_value(self):
#         if self.form.is_valid():
#             return self.form.cleaned_data.get("search")
#
#
# class ProjectView(DetailView):
#     template_name = "projects/project_view.html"
#     model = Project
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['issues'] = self.object.comments.order_by("-update_at")
#         return context
#
#
# class CreateProject(CreateView):
#     form_class = ProjectForm
#     template_name = "projects/create.html"
#
#     def form_valid(self, form):
#         project = form.save(commit=False)
#         project.save()
#         form.save_m2m()
#         return redirect("project_view", pk=project.pk)
#
#
# class UpdateProject(FormView):
#     form_class = ProjectForm
#     template_name = "projects/update.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         self.project = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return reverse("project_view", kwargs={"pk": self.project.pk})
#
#     def get_form_kwargs(self):
#         form_kwargs = super().get_form_kwargs()
#         form_kwargs['instance'] = self.project
#         return form_kwargs
#
#     def form_valid(self, form):
#         self.project = form.save()
#         return super().form_valid(form)
#
#     def get_object(self):
#         return get_object_or_404(Project, pk=self.kwargs.get("pk"))
#
#
# class DeleteProject(View):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs['pk']
#         project = get_object_or_404(Project, pk=pk)
#         return render(request, 'issues/delete.html', {'project': project})
#
#     def post(self, request, *args, **kwargs):
#         pk = kwargs['pk']
#         project = get_object_or_404(Project, pk=pk)
#         project.delete()
#         return redirect('index')


from django.shortcuts import redirect, get_object_or_404, render
# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, FormView
from django.views.generic import ListView

from webapp.forms import ProjectForm
from webapp.models import Issue
from webapp.models import Project


class IndexView(ListView):
    model = Issue
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = "-updated_at"
    paginate_by = 3


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.object.projects.order_by("-created_at")
        return context


class CreateProject(CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        return redirect("ProjectView", pk=project.pk)


class UpdateProject(FormView):
    form_class = ProjectForm
    template_name = "projects/update.html"

    def dispatch(self, request, *args, **kwargs):
        self.project = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("ProjectView", kwargs={"pk": self.project.pk})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['instance'] = self.project
        return form_kwargs

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(Project, pk=self.kwargs.get("pk"))


class DeleteProject(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        return render(request, 'projects/delete.html', {'project': project})

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return redirect('index')
