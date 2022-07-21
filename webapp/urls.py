from django.urls import path
from django.views.generic import RedirectView

from webapp.views import IndexView, IssueView, CreateIssue, UpdateIssue, DeleteIssue

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('issue/', RedirectView.as_view(pattern_name='index')),
    path('issue/<int:pk>', IssueView.as_view(), name='IssueView'),
    path('issue/create/', CreateIssue.as_view(), name='CreateIssue'),
    path('issue/update/<int:pk>/', UpdateIssue.as_view(), name='UpdateIssue'),
    path('issue/delete/<pk>/', DeleteIssue.as_view(), name='DeleteIssue'),
]
