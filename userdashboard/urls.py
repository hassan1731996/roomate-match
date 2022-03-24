from django.conf.urls import url
from userdashboard.views import *

urlpatterns = [
    url('login/', DashboardLoginView.as_view(), name="LoginView"),
    url('dashboard/', DashboardIndexView.as_view(), name="DashboardView"),
    url('logout/', DashboardLogoutView.as_view(), name='LogoutView'),
    url('signup/', DashboardRegisterView.as_view(), name='SignupView'),
    url('(?P<post_id>\d+)/', DashboardGetPost.as_view(), name='GetPostView'),
]
