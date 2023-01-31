
from django.shortcuts import render,redirect


from django.shortcuts import render

from rest_framework.response import  Response
from rest_framework.views import APIView
# from .utils import get_tokens_for_user

from django.views import View
from .models import Post,comment
from .forms import PostForm,CommentForm

from rest_framework import status

from rest_framework.response import  Response
from rest_framework.views import APIView
# from .utils import get_tokens_for_user

# Create your views here.
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
# from .utils import get_tokens_for_user
from .serializers import RegistrationSerializer, PasswordChangeSerializer
# Create your views here.
import csv

# Create your views here.

import csv

# Create your views here.

def exportcsv(request):
    students = Product.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'image', 'name', 'price', 'date'])
    studs = students.values_list('id','image', 'name', 'price', 'date')
    for std in studs:
        writer.writerow(std)
    return response
def threads(request):
    return render(request,'threads.html')
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
def index(request):
        
        category= Category.objects.all()
        brandId = request.GET.get('brand')
        CategoryId = request.GET.get('category')
        if CategoryId:
            product = Product.objects.filter(sub_category=CategoryId).order_by('-id')
        elif brandId:
            product = Product.objects.filter(brand=brandId).order_by('-id')

        else:
            product=Product.objects.all()

        context={
            "category":category,
            
            "product":product
        }
        return render(request,'index.html',context)
def logout_view(request):
    logout(request)
    return redirect('/auth/login/')
def contect(request):
    if request.method =="POST":
        contect = contect_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contect.save()
    return render(request,'contect.html')
class PostListView( View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'post_list.html', context)
class PostDetailView( View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()

        comments = comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'post_detail.html', context)
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = comment.objects.filter(post=post).order_by('-created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'post_detail.html', context)



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)



