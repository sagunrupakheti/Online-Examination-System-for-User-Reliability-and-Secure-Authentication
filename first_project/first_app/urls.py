from django.contrib import admin
from django.urls import path, include
from first_app import views

app_name = 'first_app'

urlpatterns = [
    path('', views.index, name='index'),
    #path('',views.registerUser,name='registerUser'),
    #path('first_app',include('first_app.urls')),
    path('user_login',views.user_login,name='user_login'),
    path('',views.teacherListView,name='list'),
    path('',views.studentListView,name='list'),
    path('updateTeacher/<str:pk>/',views.updateTeacher,name='updateTeacher'),
    path('video_feed',views.video_feed, name='video_feed'),
    path('click_pic',views.click_pic, name='click_pic'),
    path('face_feed',views.face_feed, name='face_feed'),
]
