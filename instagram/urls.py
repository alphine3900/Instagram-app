from django.urls import path
from instagram import views
from django.shortcuts import render

urlpatterns = [
    path('',views.landingpage,name='landingpage'),
    path('home',views.home,name='home'),
     path('login',views.login_view, name='login'),
      path('register',views.register_view, name='register'),
    path('profile',views.profile, name='profile'),
    path('like/<int:image_id>',views.likes,name='likes'),
   path('comment/<int:image_id>',views.comments,name='comments'),
    path('upload',views.uploadPic,name='upload'),
  path('update-profile/',views.updateProfile,name='editProfile'),
  path('search/', views.search_results,name='search_results'),
]
