from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mainweb.models import UserPosts
from userdashboard.models import ApplicationUsers
from userdashboard.serializers import UserPostsSerializer


class DashboardRegisterView(View):

    def get(self, request):
        return render(request, 'user-dashboard/pages/register.html')

    def post(self, request):
        try:
            if request.method == 'POST':
                user = User()
                user.username = request.POST.get('username')
                user.set_password(request.POST.get('password'))
                user.email = request.POST.get('email')
                user.save()
                if user:
                    ApplicationUsers.objects.create(user_id=user.id, phone=request.POST.get('phone'),
                                                    university=request.POST.get('university'))
                    login(request, user)
                    return redirect('account:DashboardView')
                else:
                    return render(request, "user-dashboard/pages/register.html",
                                  context={"errors": "Error creating account"})
        except Exception as e:
            return render(request, "user-dashboard/pages/register.html", context={"errors": str(e)})


class DashboardLoginView(View):

    def get(self, request):
        return render(request, 'user-dashboard/pages/login.html')

    def post(self, request):
        if request.method == "POST":
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect('account:DashboardView')
            else:
                return render(request, 'user-dashboard/pages/login.html',
                              context={"errors": "Login credentials are wrong"})


class DashboardIndexView(LoginRequiredMixin, View):

    def get(self, request):
        """ Get university specific posts """
        user_uni = ApplicationUsers.objects.get(user=request.user).university
        user_posts = UserPosts.objects.filter(university=user_uni)
        return render(request, 'user-dashboard/pages/dashboard.html',
                      context={"posts": user_posts})

    def post(self, request):
        """ Creating post from dashboard view """
        post_obj = UserPosts.objects.create(user=request.user, city=request.POST.get('city'),
                                            university=request.POST.get('university'),
                                            title=request.POST.get('post_title'),
                                            looking_for=request.POST.get('looking_for'))
        if post_obj:
            return redirect('account:DashboardView')
        return render(request, 'user-dashboard/pages/login.html', context={"errors": "Error creating post"})


class DashboardLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('account:LoginView')


class DashboardGetPost(APIView):

    def get(self, request, *args, **kwargs):
        """ Get data against specific post ID """
        try:
            post_obj = UserPosts.objects.get(id=kwargs.get('post_id'))
            serializer = UserPostsSerializer(post_obj)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """ Update post via post ID """
        post_obj = UserPosts.objects.get(id=kwargs.get('post_id'))
        serializer = UserPostsSerializer(post_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
