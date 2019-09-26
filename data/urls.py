from django.urls import path
from . import views



urlpatterns = [
    path("data/",views.data_index,name="data_index"),
    path("<int:pk>/", views.data_detail, name="data_detail"),
    path("login_user/", views.login_user, name='login_user'),
    path("add_server/", views.add_server, name='add_server'),
    path("logout_user/", views.logout_user, name='logout_user'),
    path("signup/", views.signup, name='signup'),
    path("show_search/", views.show_search, name='show_search'),
    path("show_server_data/", views.show_server_data, name='show_server_data'),
    path("check_users/", views.check_users, name='check_users'),
    path("run_command/", views.run_command, name='run_command'),
]

