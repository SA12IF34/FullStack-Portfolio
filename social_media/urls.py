from django.urls import path
from .views import *

urlpatterns = [
    path('token/', CsrfTokenAPI.as_view()),
    path('create-account/', RegisterAPI.as_view()),
    path('login/', AuthenticationAPI.as_view()),
    path('logout/', LogOutAPI.as_view()),
    path('close-account/', CloseAPI.as_view()),
    path('accounts/', AccountsAPI.as_view()),
    path('accounts/<int:id>/', AccountAPI.as_view()),
    path('search/<str:term>/', SearchAPI.as_view()),
    path('me/', AccountAPI.as_view()),
    path('followers/', FollowersAPI.as_view()),
    path('follow/', FollowsAPI.as_view()),
    path('unfollow/', UnfollowAPI.as_view()),
    path('posts/', PostsAPI.as_view()),
    path('posts/type/<str:type>/', PostsAPI.as_view()),
    path('posts/author/<int:author>/', PostsAPI.as_view()),
    path('posts/<int:id>/', PostAPI.as_view()),
    path('posts/<int:id>/edit/', PostEditAPI.as_view()),
    path('like/<int:id>/', LikeAPI.as_view()),
    path('dislike/<int:id>/', DislikeAPI.as_view()),
    path('comments/<int:post>/', CommentsAPI.as_view()),
    path('comment/<int:pk>/', CommentAPI.as_view())
]