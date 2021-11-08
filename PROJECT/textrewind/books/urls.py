from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.user_signup),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('catalog/', views.catalog),
    path('my_books/', views.my_books),
    path('new_book/', views.new_book, name='new_book'),
    path('add/<int:id>/', views.book_addition),
    path('book/<int:id>/', views.book_view, name='book'),
    path("search/", views.Search.as_view(), name='search'),
    path('', views.index),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]