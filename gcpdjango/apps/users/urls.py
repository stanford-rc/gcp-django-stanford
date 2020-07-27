
from django.urls import path
from django.conf.urls import url, include
import gcpdjango.apps.users.views as views

urlpatterns = [
    # Twitter, and social auth
    url(r"^login/$", views.login, name="login"),
    url(r"^accounts/login/$", views.login),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^password/$", views.change_password, name="change_password"),
    url(r"^terms/agree", views.agree_terms, name="agree_terms"),
    url(r"^u/delete$", views.delete_account, name="delete_account"),  # delete account
    url(r"^u/profile", views.view_profile, name="profile"),
    # Groups
    path("group/<int:uuid>/", views.group_details, name="group_details"),
    path("groups/", views.all_groups, name="all_groups"),
    path("u/group/", views.user_group, name="user_group"),
    # Users
    path("u/invite/", views.invite_users, name="invite_users"),
    path("u/invite/<uuid:uuid>", views.invited_user, name="invited_user"),
    # We don't currently have a reason for one user to see another user's account
    # url(r'^(?P<username>[A-Za-z0-9@/./+/-/_]+)/$',views.view_profile,name="profile"),
]
