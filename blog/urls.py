from django.urls import path
from .views import (
    signup,
    login,
    BlogListAPIView,          #updated
    blog_detail,
    comment_list_create,
    comment_update,
    comment_delete,
    like_toggle, 
    home,
    login_frontend,
    logout_frontend,
    signup_frontend
)

urlpatterns = [

    # -----------------------------
    # FRONTEND URLS
    # -----------------------------
    path('', home, name='home'),
    path('login/', login_frontend, name='login_frontend'),
    path('logout/', logout_frontend, name='logout_frontend'),
    path('signup/', signup_frontend, name='signup_frontend'),

    # -----------------------------
    # API URLS (🔥 CHANGE HERE)
    # -----------------------------
    path('auth/signup/', signup, name='api-signup'),
    path('auth/login/', login, name='api-login'),
    
    
    
    # BLOG APIs
    path('blogs/', BlogListAPIView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', blog_detail, name='blog-detail'),

    # COMMENT APIs
    path('blogs/<int:blog_id>/comments/', comment_list_create),
    path('comments/<int:comment_id>/', comment_update),
    path('comments/<int:comment_id>/delete/', comment_delete),

    # LIKE API
    path('blogs/<int:blog_id>/like/', like_toggle),
]