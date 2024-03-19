from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    # User Profile
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile_edit/', views.UserEditView.as_view(), name='user_profile_edit'),
    # Authentication
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    # password reset
    path('reset_password/', views.UserPasswordResetView.as_view(), name='user_password_reset'),
    path('reset_password/done/', views.UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='user_password_reset_confirm'),
    path('reset_password/complete/', views.UserPasswordResetCompleteView.as_view(),
         name='user_password_reset_complete'),
    # Users Relations
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnfollowView.as_view(), name='user_unfollow'),
]
