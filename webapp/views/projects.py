from django.contrib.auth.mixins import LoginRequiredMixin
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
    paginate_by = 5


class ProjectView(DetailView):
    template_name = "projects/project_view.html"
    model = Project

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['projects'] = self.object.projects.order_by("-created_at")
        # return context

        pk = self.kwargs.get("pk")
        users = User.objects.filter(projects__pk=pk)
        context = super().get_context_data(**kwargs)
        context["users"] = users
        return context


class AddUsers(UpdateView):
    model = Project
    form_class = AddUsersForm
    template_name = 'add_users_view.html'


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = "projects/create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        return redirect("webapp:ProjectView", pk=project.pk)

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect("accounts:login")


class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'projects/update.html'
    form_class = ProjectForm
    context_object_name = 'project'


class DeleteProject(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/delete.html"
    success_url = reverse_lazy("webapp:index")
