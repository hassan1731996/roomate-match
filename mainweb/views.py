from django import template
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView

from mainweb.models import UserPosts, UserRegistration, ImageModel, UserContacts
from userdashboard.models import ApplicationUsers


class MainWebIndexView(View):

    def get(self, request):
        # Get only latest 3 posts for index page
        users_posts = UserPosts.objects.all()[:3]
        return render(request, 'main-web/pages/index.html', context={"users_posts": users_posts})


class MainWebLoginView(View):
    def get(self, request):
        return render(request, 'main-web/pages/user-login.html')

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('mainweb:UserPostsView')
        else:
            return render(request, 'main-web/pages/user-login.html', context={"error": "Invalid Credentials."})


class MainWebLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('mainweb:Index')


class MainWebUserSignup(View):

    def get(self, request):
        all_uni = ApplicationUsers.objects.all().values('university')
        return render(request, 'main-web/pages/user-signup.html', context={'universities': all_uni})

    def post(self, request):
        try:
            user = User()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password'))
            user.email = request.POST.get('email')
            user.save()
            if user:
                UserRegistration.objects.create(user_id=user.id, age=request.POST.get('age'),
                                                gender=request.POST.get('gender'),
                                                university=request.POST.get('university'),
                                                classification=request.POST.get('classification'))
                login(request, user)
                return redirect('mainweb:UserPostsView')
            return render(request, 'main-web/pages/user-signup.html', context={'error': 'Error creating user'})
        except Exception as e:
            return render(request, 'main-web/pages/user-signup.html', context={'error': str(e)})


class MainWebGetAllPostsView(View):
    """Get all posts i.e(even when user is logged In, he wants to see all posts)"""

    def get(self, request):
        posts_list = UserPosts.objects.all()
        page = request.GET.get('page', 1)
        # by default only six posts will be rendered
        paginator = Paginator(posts_list, 6)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'main-web/pages/all-posts.html', {'all_posts': posts})


class MainWebPostsView(View):
    """Get post against specific username"""

    def get(self, request):
        posts_list = UserPosts.objects.filter(user_reg__user__username=request.user.username)
        page = request.GET.get('page', 1)
        # by default only six posts will be rendered
        paginator = Paginator(posts_list, 6)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'main-web/pages/user-posts.html', {'all_posts': posts})


class MainWebGetPost(View):

    def get(self, request, *args, **kwargs):
        """ GET specific post """
        try:
            post_obj = UserPosts.objects.get(id=kwargs.get("post_id"))
            posts_images = ImageModel.objects.filter(image__id=kwargs.get("post_id"))
            if request.GET.get('edit'):
                return render(request, 'main-web/pages/user-edit-post.html',
                              context={'data': post_obj, 'posts_images': posts_images})
            return render(request, 'main-web/pages/post-single.html',
                          context={'data': post_obj, 'posts_images': posts_images})
        except UserPosts.DoesNotExist:
            return HttpResponse("PostID not found", status=404)


class MainWebCreatePost(View):
    def get(self, request):
        all_uni = UserRegistration.objects.all().values('university')
        return render(request, 'main-web/pages/user-create-post.html', context={'universities': all_uni})

    def post(self, request, *args):
        """ Create post for requested user """
        post_created = UserPosts.objects.create(
            user_reg_id=request.user.userregistration_set.get(user_id=request.user.id).id,
            looking_for=request.POST.get('looking_for'), move_in=request.POST.get('move_in'),
            housing_type=request.POST.get('housing_type'), date=request.POST.get('date'),
            no_of_bedrooms=request.POST.get('no_bedrooms') if request.POST.get('no_bedrooms') else 0,
            no_of_bathrooms=request.POST.get('no_bathrooms') if request.POST.get('no_bathrooms') else 0)

        if post_created and request.POST.get('looking_for') == 'ROOMMATES':
            if request.FILES:
                for image in request.FILES.getlist('pics'):
                    ImageModel.objects.create(image_id=post_created.id, main_image=image)
                return redirect('mainweb:UserPostsView')
            return render(request, 'main-web/pages/user-create-post.html', context={'error': 'Error creating post'})
        else:
            return redirect('mainweb:UserPostsView')


class MainWebEditDeletePost(APIView):
    """ Edit/Delete specific post"""

    def get(self, request, *args, **kwargs):
        try:
            UserPosts.objects.get(id=kwargs.get('post_id')).delete()
            return redirect('mainweb:UserPostsView')
        except ObjectDoesNotExist:
            return render(request, 'main-web/pages/user-edit-post.html', context={"error": "ID not found"})

    def post(self, request, *args, **kwargs):
        try:
            post_obj = UserPosts.objects.get(id=kwargs.get('post_id'))
            post_obj.looking_for = request.POST.get('looking_for')
            post_obj.role = request.POST.get('status')
            post_obj.move_in = request.POST.get('move_in')
            post_obj.housing_type = request.POST.get('housing_type')
            post_obj.date = request.POST.get('date')
            post_obj.no_of_bedrooms = request.POST.get('no_bedrooms') if request.POST.get('no_bedrooms') else 0
            post_obj.no_of_bathrooms = request.POST.get('no_bathrooms') if request.POST.get('no_bathrooms') else 0
            post_obj.save()
            if post_obj and request.POST.get('looking_for') == 'ROOMMATES':
                if request.FILES:
                    for image in request.FILES.getlist('pics'):
                        img_obj = ImageModel()
                        img_obj.image_id = post_obj.id
                        img_obj.main_image = image
                        img_obj.save()
                    return redirect('mainweb:UserPostsView')
                else:
                    return redirect('mainweb:UserPostsView')
            else:
                return redirect('mainweb:UserPostsView')
        except Exception as e:
            return render(request, 'main-web/pages/user-edit-post.html', context={'error': str(e)})


class MainWebContactView(View):

    def get(self, request):
        contacts = UserContacts.objects.filter(user=request.user)
        return render(request, 'main-web/pages/user-contacts.html', context={'contacts': contacts})

    def post(self, request):
        # TODO once get SMTP-credentials rest of the work needs to be done here
        message = request.POST.get('message', None)
        post_id = request.POST.get('post_id', None)
        try:
            post_obj = UserPosts.objects.get(id=post_id)
            UserContacts.objects.create(user=request.user, message=message, contacted_for=post_obj)
            return redirect('mainweb:ContactView')
        except ObjectDoesNotExist:
            return HttpResponse('Error contacting!')


class MainWebSearchView(View):

    def post(self, request, *args, **kwargs):
        gender = request.POST.get('gender', None)
        move_in = request.POST.get('move_in', None)
        university = request.POST.get('university', None)
        posts_list = []
        if gender:
            posts_list = UserPosts.objects.filter(user_reg__gender=gender)
        if move_in:
            posts_list = UserPosts.objects.filter(date__exact=move_in)
        if university:
            posts_list = UserPosts.objects.filter(user_reg__university=university)
        if gender and move_in:
            posts_list = UserPosts.objects.filter(Q(date__exact=move_in) & Q(user_reg__gender=gender))
        if gender and university:
            posts_list = UserPosts.objects.filter(Q(user_reg__university=university) & Q(user_reg__gender=gender))
        if move_in and university:
            posts_list = UserPosts.objects.filter(Q(user_reg__university=university) & Q(date__exact=move_in))
        if gender and move_in and university:
            posts_list = UserPosts.objects.filter(
                Q(user_reg__university=university) & Q(date__exact=move_in) & Q(user_reg__gender=gender))

        page = request.GET.get('page', 1)
        # by default only six posts will be rendered
        paginator = Paginator(posts_list, 6)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return render(request, 'main-web/pages/all-posts.html', {'all_posts': posts})
