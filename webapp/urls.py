from django.urls import path

from webapp.views import IndexView, IssueView, CreateIssue, UpdateIssue, DeleteIssue

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('issue/<issue_pk>', IssueView.as_view(), name='IssueView'),
    path('create/', CreateIssue.as_view(), name='CreateIssue'),
    path('product/<int:pk>/update/', UpdateIssue.as_view(), name='UpdateIssue'),
    path('product/<pk>/delete/', DeleteIssue.as_view(), name='DeleteIssue'),
]
