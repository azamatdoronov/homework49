from django.urls import path
from django.views.generic import RedirectView

from webapp.views import IndexView, IssueView, CreateIssue, UpdateIssue, DeleteIssue, CreateProject, ProjectView, \
    IndexIssueView, UpdateProject, DeleteProject

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('project/<int:pk>', ProjectView.as_view(), name='ProjectView'),
    path('issue/', IndexIssueView.as_view(), name='IndexIssueView'),
    path('issue/<int:pk>', IssueView.as_view(), name='IssueView'),
    path('issue/create/', CreateIssue.as_view(), name='CreateIssue'),
    path('issue/update/<int:pk>/', UpdateIssue.as_view(), name='UpdateIssue'),
    path('issue/delete/<pk>/', DeleteIssue.as_view(), name='DeleteIssue'),
    path('project/create/', CreateProject.as_view(), name='CreateProject'),
    path('project/update/<int:pk>/', UpdateProject.as_view(), name='UpdateProject'),
    path('project/delete/<pk>/', DeleteProject.as_view(), name='DeleteProject'),
]
