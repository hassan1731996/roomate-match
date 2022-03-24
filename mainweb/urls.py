from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MainWebIndexView.as_view(), name="Index"),
    path('register/', MainWebUserSignup.as_view(), name="UserRegister"),
    path('login/', MainWebLoginView.as_view(), name="UserLogin"),
    path('my-posts/', MainWebPostsView.as_view(), name="UserPostsView"),
    path('create/post/', MainWebCreatePost.as_view(), name="UserCreatePostView"),
    path('edit/post/<int:post_id>/', MainWebEditDeletePost.as_view(), name="UserEditDeletePostView"),
    path('all-posts/', MainWebGetAllPostsView.as_view(), name="AllPostsView"),
    path('post/<int:post_id>', MainWebGetPost.as_view(), name="GetPostView"),
    path('my-contacts/', MainWebContactView.as_view(), name="ContactView"),
    path('logout/', MainWebLogoutView.as_view(), name="LogoutView"),
    path('search/', MainWebSearchView.as_view(), name="SearchView"),
]
