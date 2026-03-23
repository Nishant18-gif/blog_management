from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from rest_framework.generics import ListCreateAPIView

from .models import Blog, Comment, Like
from .serializers import BlogSerializer, CommentSerializer


# -----------------------------
# FRONTEND HOME PAGE
# -----------------------------
def home(request):
    blogs = Blog.objects.filter(
        deleted_at__isnull=True
    ).prefetch_related('comments', 'likes').order_by('-id')

    return render(request, 'index.html', {'blogs': blogs})


# -----------------------------
# FRONTEND LOGIN / LOGOUT / SIGNUP
# -----------------------------
def login_frontend(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        return render(request, 'index.html', {
            'blogs': Blog.objects.all(),
            'error': 'Invalid username or password'
        })
    return redirect('home')


def logout_frontend(request):
    logout(request)
    return redirect('home')


def signup_frontend(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'index.html', {
                'blogs': Blog.objects.all(),
                'signup_error': 'Both fields are required'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'index.html', {
                'blogs': Blog.objects.all(),
                'signup_error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('home')

    return redirect('home')


# -----------------------------
# API SIGNUP
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


# -----------------------------
# API LOGIN
# -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)


# -----------------------------
# BLOG LIST + CREATE
# -----------------------------
class BlogListAPIView(ListCreateAPIView):
    queryset = Blog.objects.filter(
        deleted_at__isnull=True,
        status='published'
    ).order_by('-id')

    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -----------------------------
# BLOG DETAIL / UPDATE / DELETE
# -----------------------------
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id=pk)

    if request.method in ['PUT', 'DELETE']:
        if request.user != blog.author:
            return Response({"error": "Not allowed"}, status=403)

    if request.method == 'GET':
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        blog.deleted_at = timezone.now()
        blog.save()
        return Response({"message": "Blog soft deleted"}, status=204)


# -----------------------------
# COMMENT CREATE / LIST
# -----------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(blog=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if request.user != blog.author:
            return Response({"error": "Only blog author can comment"}, status=403)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, blog=blog)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# -----------------------------
# COMMENT UPDATE
# -----------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# -----------------------------
# COMMENT DELETE
# -----------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return Response({"message": "Comment deleted successfully"}, status=204)


# -----------------------------
# LIKE / UNLIKE TOGGLE
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_toggle(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        like.delete()
        return Response({
            "liked": False,
            "likes_count": blog.likes.count()
        })

    return Response({
        "liked": True,
        "likes_count": blog.likes.count()
    })