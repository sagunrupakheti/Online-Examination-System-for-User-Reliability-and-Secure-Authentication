"""first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from first_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('loginPage',views.index,name='loginPage'),
    path('index', include('first_app.urls')),
    path('admin/', admin.site.urls),
    path('help', views.help, name='asd'),
    path('static', include('first_app.urls')),
    path('first_app', include('first_app.urls')),
    path('user_login',views.user_login,name='user_login'),
    path('login', views.goLogin, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('adminDashboard', views.adminDashboard, name='dashboard'),
    path('adminDashboard00', views.adminDashboard00, name='dashboardx'),
    path('teacherDashboard', views.teacherDashboard, name='teacher_dashboard'),
    path('studentDashboard', views.studentDashboard, name='student_Dashboard'),
    path('studentDashboard00', views.studentDashboard00, name='student_Dashboard00'),
    path('teacherDashboard00', views.teacherDashboard00, name='teacher_dashboard00'),
    path('teacherExamList', views.examListView, name='teacherExamList'),
    path('studentExamList', views.examListViewStudent, name='student_exam'),
    path('manageExam', views.form_add_exam, name='exam'),
    path('updateExam/<exam_id>', views.update_exam, name='updateExam'),
    path('deleteExam/<exam_id>', views.delete_exam, name='deleteExam'),
    path('manageExamContent/<examId>', views.form_add_exam_content, name='exam_content'),
    path('asd', views.asd, name='asd'),
    path('registerUser',views.registerUser,name='registerUser'),
    path('updateTeacher/<userId>',views.updateTeacher,name='updateTeacher'),
    path('updateCourse/<str:pk>/',views.updateCourse,name='updateCourse'),
    path('deleteCourse/<str:pk>/',views.deleteCourse,name='deleteCourse'),
    path('logout',views.user_logout,name='logout'),
    path('studentList',views.studentListView,name='std_list'),
    path('setExamInfoTeacher/<exam_id>',views.setExamInfo,name='setExamInfoTeacher'),
    path('teacherList',views.teacherListView,name='teacher'),
    path('manageCourse',views.form_add_course,name='manageCourse'),
    path('deleteUser/<userId>',views.deleteUser,name='deleteUser'),
    path('addDashBoardInfoAdmin',views.addDashBoardInfoAdmin,name='addDashBoardInfoAdmin'),
    path('giveExam/<examId>',views.giveExam,name='giveExam'),
    path('makeExamLive/<examId>',views.makeExamLive,name='makeExamLive'),
    path('authenticate_user/<examId>',views.authenticate_user,name='authenticateUser'),
    path('showPasswordView/<examId>',views.showPasswordView,name='showPasswordView'),
    path('manageResult/<examId>',views.manageResult,name='manageResult'),
    path('expiredExams',views.givenExams, name='expiredExams'),
    path('changeResultVisibility/<id>',views.changeResultVisibility, name='changeResultVisibility'),
    path('changeResultVisibilityReverse/<id>',views.changeResultVisibilityReverse, name='changeResultVisibilityReverse'),
    path('showResultStudent',views.showResultStudent,name='showResultStudent'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('showCamera', views.showCamera, name='showCamera'),
    path('picsCollect', views.picsCollect, name='picsCollect'),
    path('facialRecognition', views.facialRecognition, name='facialRecognition'),
    path('updatePasswordTeacher', views.updatePasswordTeacher, name='updatePasswordTeacher'),
    path('updatePasswordStudent', views.updatePasswordStudent, name='updatePasswordStudent'),
    path('checkAuthenticateUser',views.checkAuthenticateUser,name='checkAuthenticateUser'),
    path('student_info', views.send_profile_info_student, name='student_info'),
    path('teacher_info', views.send_profile_info_teacher, name='teacher_info'),
    path('admin_info', views.send_profile_info_admin, name='admin_info'),
    path('makeExamExpire/<exam_id>', views.makeExamExpire, name='makeExamExpire'),
    path('showPaperDetailsTeacher/<exam_id>/<student_id>',views.showPaperDetailsTeacher,name='showPaperDetailsTeacher'),
    path('error',views.error, name='error'),
    path('face_feed',views.face_feed, name='face_feed'),
    path('allNotification',views.view_notification,name='allNotification'),
]+static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
