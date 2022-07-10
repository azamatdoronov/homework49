from django.urls import path
from django.views.generic import RedirectView

from webapp.views import IndexView, create_issue, IssueView, update_issue, delete_issue

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('issue/', RedirectView.as_view(pattern_name="index")),
    path('issue/add/', create_issue, name="create_issue"),
    path('issue/<int:pk>/', IssueView.as_view(extra_context={"test": 5}), name="issue_view"),
    path('issue/<int:pk>/update/', update_issue, name="update_issue"),
    path('issue/<int:pk>/delete/', delete_issue, name="delete_issue"),
]
