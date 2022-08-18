from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic import ListView

from webapp.forms import ProjectForm, AddUsersForm
from webapp.models import Project


class IndexView(ListView):
    model = Project
    template_name = "projects/index.html"
    context_object_name = "projects"
    ordering = "-start_date"
    paginate_by = 6


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk")
        projects = User.objects.filter(projects__pk=pk)
        context = super().get_context_data(**kwargs)
        context["projects"] = self.object.projects.order_by("-created_at")
        context["users"] = projects
        return context


class AddUsers(UpdateView):
    model = Project
    form_class = AddUsersForm
    template_name = 'add_users_view.html'

    def has_permission(self):
        return self.request.user.has_perm("webapp.add_user") or \
               self.request.user == self.get_object().users


class ViewUsers(ListView):
    model = get_user_model()
    template_name = 'projects/users_view.html'
    context_object_name = "users"
    paginate_by = 6
    paginate_orphans = 0

    def has_permission(self):
        return self.request.user.has_perm("webapp.users_view") or \
               self.request.user == self.get_object().users


class CreateProject(PermissionRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        return redirect("webapp:ProjectView", pk=project.pk)

    def has_permission(self):
        return self.request.user.has_perm("webapp.create_project") or \
               self.request.user == self.get_object().users

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect("accounts:login")


class UpdateProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'
    form_class = ProjectForm
    context_object_name = 'project'

    def has_permission(self):
        return self.request.user.has_perm("webapp.update_project") or \
               self.request.user == self.get_object().users


class DeleteProject(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy("webapp:index")

    # return self.request.user.is_superuser or \
    #        self.request.user.groups.filter(name__in=("Модераторы",)).exists()

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, instance=self.get_object())
        if form.is_valid():
            return self.delete(request, *args, **kwargs)
        else:
            return self.get(request, *args, **kwargs)

    def has_permission(self):
        return self.request.user.has_perm("webapp.remove_project") or \
               self.request.user == self.get_object().users
