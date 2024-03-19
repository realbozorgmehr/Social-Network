from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # Posts Management
    path('detail/<slug:post_slug>/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_craete/', views.PostCreateView.as_view(), name='post_create'),
    path('post/update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
    # comments
    path('comment/reply/<int:post_id>/<int:comment_id>/', views.CommentReplyAddView.as_view(), name='comment_reply'),
    # Likes
    path('like/<int:post_id>/', views.PostLikeView.as_view(), name='post_like'),
]
