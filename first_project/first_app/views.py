import datetime
import time
from random import shuffle

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from .camera import VideoCamera
from .faceDetect import checkFace
from .models import User, Course, Teacher, FinalResult, UserProfileInfo, Student, \
    Examination, \
    Question, ExamAttendance, SamplePicsStatus, AuthenticateExam, Notification
from . import forms
from .forms import UserForm, UserProfileInfoForm, CourseForm, manageTeacherForm, QuestionAdd, \
    editExamTeacherForm, ExaminationAdd, SubjectiveQuestionAdd, responseForm, UserProfileUpdatePic

# for login\
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.forms import inlineformset_factory, formset_factory
from django.contrib.auth.hashers import make_password, check_password
from .models import Response, CalculatedMark
from django.db.models import Sum, Count
from django.db.models import Q
from .filters import StudentFilter, ExamFilter
from .decorators import authenticated_user, check_teacher_authentication, check_super_user, check_student_authentication
from django.contrib import messages
# date comparison
import pytz

utc = pytz.UTC
getReq = 'req'

#convert to string
def to_str(value):
    return str(value)


#check int
def int_or_0(value):
    try:
        return int(value)
    except:
        return 0


def index(request):
    return render(request, 'index.html', {})


def goLogin(request):
    logout(request)
    return render(request, 'index.html', {})

@login_required(login_url='index')
def user_logout(request):
    logout(request)
    return redirect('index')


# login method
def user_login(request):
    global getReq
    if request.method == 'POST':
        # username in login view
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.all().filter(username=username)
        profile = UserProfileInfo.objects.filter(user__in=users).values('userType').first()
        getFinal = ''
        if (profile != None):
            getFinal = profile.get('userType')
        # for authentication
        user = authenticate(username=username, password=password)
        # if the user if a teacher
        if user and getFinal == 'Teacher':
            if user is not None:
                # first time login
                if user.last_login is None:
                    # if user is active
                    login(request, user)
                    return HttpResponseRedirect('updatePasswordTeacher')
                else:
                    login(request, user)
                return HttpResponseRedirect('teacherDashboard00')
        # if the user is a student
        elif user and getFinal == 'Student':
            if user is not None:
                # first time login
                if user.last_login is None:
                    login(request, user)
                    getReq = request.user
                    return HttpResponseRedirect('updatePasswordStudent')
                    # return HttpResponseRedirect('showCamera')
                else:
                    login(request, user)
                    # return HttpResponseRedirect('showCamera')
                    return HttpResponseRedirect('studentDashboard00')
            else:
                messages.info(request, 'Incorrect Credentials')
            return HttpResponse('Please enter correct credentials')
        elif user:
            if user is not None:
                # if user is active
                login(request, user)
                return HttpResponseRedirect('adminDashboard00')
            else:
                messages.info(request, 'Incorrect Credentials')
            return HttpResponse('Please enter correct credentials')
        else:
            messages.error(request, 'Incorrect Credentials')
            return redirect('index')

        return render(request, 'index.html', {})

@login_required(login_url='index')
def registerUser(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        try:
            user = user_form.save() #save username
            user.set_password(user.password) #set the password
            user.save()  #save the final data
            profile = profile_form.save(commit=False)# one to one relationship
            profile.user = user #add the foreign key element
            email = request.POST.get('email')
            user_type = request.POST.get('userType')  #get the user type of the user
            if ('profile_pic' in request.FILES): #if profile pic has been added
                profile.profile_pic = request.FILES['profile_pic'] #add the picture file
                profile.save() #save the data
                registered = True #boolean set to true
                id = UserProfileInfo.objects.latest('user') #get the recently added user
                course_id = request.POST.get('course_id') #get the user's course code
                course = Course.objects.all().filter(course_id=course_id)

                if (user_type == "Teacher"): #add in teacher table
                    addAsTeacher(id, course)
                elif (user_type == "Student"): #add in student table
                    addAsStudent(id, course)
                send_mail('Your registration for EXAMIC examination system has been confirmed!','Your Username is: ' + request.POST.get('username')+ ' and your password is: '+ request.POST.get('password')
                          ,'sagunrupakheti@gmail.com',[request.POST.get('email')],fail_silently=False)
                messages.success(request, 'Successfully added user! An email has been sent to notify the user.')
                return redirect('registerUser')
        except Exception as e:
            print('yo error ho',type(e))
            if type(e)==ValueError:
                messages.error(request, 'Cannot add a future birthdate!')
            else:
                messages.error(request, 'Please add a unique username!')
            return redirect('registerUser')
    else:#send the data if not post method
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    notification = Notification.objects.all()
    return render(request, 'registerUser.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'notification':notification})

@login_required(login_url='index')
@check_super_user
def adminDashboard(request):
   user = User.objects.all().filter(username=request.user).first()
   userinfo = UserProfileInfo.objects.all().filter(user=user)
   print(userinfo)

   return render(request, 'adminDashboard.html', {'userInfo':userinfo})


@login_required(login_url='index')
@check_super_user
def adminDashboard00(request):
    # user = User.objects.all().filter(username=request.user)
    teacher_id = UserProfileInfo.objects.all().values('firstName')
    print(teacher_id)
    # getCourse = teacher_id.course_id
    notification = Notification.objects.all()
    course_list = Course.objects.all().count
    exam_list = Examination.objects.all().count
    teacher_list = UserProfileInfo.objects.all().filter(userType='Teacher').count
    student_list = UserProfileInfo.objects.all().filter(userType='Student').count
    course = UserProfileInfo.objects.all().values('course_id','course_id__course_name').annotate(total=Count('firstName'))
    user_type = UserProfileInfo.objects.all().values('userType').annotate(
        total=Count('firstName')).order_by('userType')
    print(course)
    return render(request, 'adminDashboard00.html', {'course_list': course_list, 'exam_list': exam_list,
                                                     'teacher_list': teacher_list, 'student_list': student_list,'notification':notification,
                                                     'course':course,'userType':user_type})
def view_notification(request):
    users = User.objects.all().filter(username=request.user).first()
    profile = UserProfileInfo.objects.get(user=users)
    print(profile.userType)
    notification=''
    temp=''
    if profile.userType == 'admin':
        notification = Notification.objects.all().order_by('-id')
        temp = 'adminDashboard.html'
    elif profile.userType == "Teacher":
        notification = Notification.objects.all().filter(user_type='Teacher',course_id=profile.course_id).order_by('-id')
        temp = 'teacherDashboard.html'
    elif profile.userType == "Student":
        notification = Notification.objects.all().filter(user_type='Student',course_id=profile.course_id).order_by('-id')
        temp = 'studentDashboard.html'
    return render(request,'allNotification.html', {'notification':notification,'temp':temp})

@login_required(login_url='index')
@check_super_user
def addAsTeacher(id, course_id):
    course = Course.objects.all().filter(course_id__in=course_id).first()
    teacherTable = Teacher()
    teacherTable.teacher_id = id
    teacherTable.course_id = course
    teacherTable.save()


@login_required(login_url='index')
@check_super_user
def addAsStudent(id, course_id):
    course = Course.objects.all().filter(course_id__in=course_id).first()
    studentTable = Student()
    studentTable.student_id = id
    studentTable.course_id = course
    studentTable.save()

@login_required(login_url='index')
def addExamContentOnlyIdObjective(id):
    questionTable = Question()
    questionTable.exam_id = id
    questionTable.question = "Add Question Here"
    questionTable.save()


@login_required(login_url='index')
@check_super_user
def updateTeacher(request, userId):
    users = User.objects.all().filter(username=userId).first()
    profile = UserProfileInfo.objects.all().filter(user=users).first()
    user_form = UserForm(instance=users)
    profile_form = UserProfileInfoForm(instance=profile)
    if request.method == 'POST': #post method
        user_form = UserForm(request.POST, instance=users) #create instance
        profile_form = UserProfileInfoForm(request.POST, instance=profile) #create instance
        if user_form.is_valid() and profile_form.is_valid(): #check if forms have valid data
            user_form.save() #if yes then save the forms
            profile_form.save()
            User.objects.all().filter(username=userId).update(
                password=make_password('asdfg'))
            registered = True
            if request.POST.get('userType') == 'Teacher':
                messages.success(request, 'Teacher data edited successfully!')
                return redirect('../teacherList')
            else:
                messages.success(request, 'Student data edited successfully!')
                return redirect('../studentList')
        else:
            messages.error(request, 'Please provide valid information!')
            registered = False
    registered = False
    context = {'profile_form': profile_form}
    return render(request, 'registerUser.html',
                  {
                      'profile_form': profile_form,
                      'user_form': user_form,
                      'registered': registered})


@login_required(login_url='index')
@check_super_user
def deleteUser(request, userId):
    users = User.objects.all().filter(username=userId)
    profile = UserProfileInfo.objects.all().filter(user__in=users)
    getUser = UserProfileInfo.objects.all().filter(user__in=users).first()
    teacher = Teacher.objects.all().filter(teacher_id__in=profile)
    student = Student.objects.all().filter(student_id__in=profile)
    if getUser.userType=='Teacher':
        teacher.delete()
        profile.delete()
        users.delete()
        messages.success(request, 'Teacher data deleted successfully!')
        return redirect('../teacherList')
    else:
        student.delete()
        profile.delete()
        users.delete()
        messages.success(request, 'Student data deleted successfully!')
        return redirect('../studentList')


@login_required(login_url='index')
@check_super_user
def studentListView(request):
    student = UserProfileInfo.objects.all()
    studentList = UserProfileInfo.objects.all().filter(userType="Student")
    myFilter = StudentFilter(request.POST, queryset=studentList)
    studentList  = myFilter.qs
    notification = Notification.objects.all().order_by('-id')
    return render(request, 'studentList.html', {'myFilter': myFilter,'student_dict':studentList,'notification':notification})


def asd(request):
    return render('request', 'asd.html')

def utc2local(utc):
    # takes time as tuple
    epoch = time.mktime(utc.timetuple())
    # converts the timezone aware date to normal
    offset = datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)
    return utc + offset

def checkExamStatus(request):
    exams = Examination.objects.all().filter(exam_status='Live')
    # check for exams that are live
    for i in exams.iterator():
        #check if exams have exam_time
        if i.exam_end_time is not None:
            # check if the current time is lesser or equals to the end time of the examination
            if utc2local(i.exam_end_time) < datetime.datetime.now().replace(tzinfo=utc):
                getId = i.examId
                #update the exam as expired
                Examination.objects.all().filter(examId=getId).update(exam_status='Expired')
        else:
            #else continue with the list
            continue


@login_required(login_url='index')
@check_teacher_authentication
def teacherDashboard(request):
    user = User.objects.all().filter(username=request.user)
    teacher_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = teacher_id.course_id
    notification = Notification.objects.all().filter(course_id = getCourse, user_type='Teacher').order_by('-id')
    return render(request, 'teacherDashboard.html', {'userInfo':teacher_id,'notification':notification})


@login_required(login_url='index')
@check_student_authentication
def studentDashboard(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = student_id.course_id
    notification = Notification.objects.all().filter(course_id = getCourse, user_type='Student').order_by('-id')
    return render(request, 'studentDashboard.html', {'userInfo':student_id, 'notification':notification})


@login_required(login_url='index')
@check_student_authentication
def studentDashboard00(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = student_id.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Student').order_by('-id')
    course_list = Course.objects.all().count
    exam_list = Examination.objects.all().count
    teacher_list = UserProfileInfo.objects.all().filter(userType='Teacher').count
    student_list = UserProfileInfo.objects.all().filter(userType='Student').count
    course = UserProfileInfo.objects.all().values('course_id', 'course_id__course_name').annotate(
        total=Count('firstName')).order_by('course_id')
    user_type = UserProfileInfo.objects.all().values('userType').annotate(
        total=Count('firstName')).order_by('userType')
    return render(request, 'studentDashboard00.html', {'course_list': course_list, 'exam_list': exam_list,
                                                     'teacher_list': teacher_list, 'student_list': student_list,'notification':notification,
                                                       'course':course,'userType':user_type})

@login_required(login_url='index')
@check_teacher_authentication
def teacherDashboard00(request):
    user = User.objects.all().filter(username=request.user)
    teacher_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = teacher_id.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher').order_by('-id')
    course_list = Course.objects.all().count
    exam_list = Examination.objects.all().count
    teacher_list = UserProfileInfo.objects.all().filter(userType='Teacher').count
    student_list = UserProfileInfo.objects.all().filter(userType='Student').count
    course = UserProfileInfo.objects.all().values('course_id', 'course_id__course_name').annotate(
        total=Count('firstName')).order_by('course_id')
    user_type = UserProfileInfo.objects.all().values('userType').annotate(
        total=Count('firstName')).order_by('userType')
    return render(request, 'teacherDashboard00.html', {'userInfo':teacher_id, 'course_list': course_list, 'exam_list': exam_list,
                                                     'teacher_list': teacher_list, 'student_list': student_list,'notification':notification,
                                                       'course':course,'userType':user_type})

def notificationContentTeacher(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = student_id.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher')


def addNotificationNewExam(examId):
    exams = Examination.objects.all().filter(examId=examId).first()
    notification = Notification()
    notification.course_id = exams.course_code
    notification.notification_text = 'This is to notify you that you have an upcoming examination '+exams.examName+' on '+ str(exams.exam_date)
    notification.user_type = 'Student'
    notification.save()


def addNotificationNewExamTeacher(examId):
    exams = Examination.objects.all().filter(examId=examId).first()
    notification = Notification()
    notification.course_id = exams.course_code
    notification.notification_text = 'A new examination' + exams.examName + ' has been added! '
    notification.user_type = 'Teacher'
    notification.save()


@login_required(login_url='index')
@check_teacher_authentication
def form_add_exam_content(request, examId):
    getObjectiveNum = Examination.objects.get(examId=examId)
    getSubjectiveNum = Examination.objects.get(examId=examId)
    total = int_or_0(getObjectiveNum.totalObjectiveQues)
    subTotal = int_or_0(getObjectiveNum.totalSubjectiveQues)
    QuestionFormSet = inlineformset_factory(Examination, Question, form=forms.QuestionAdd, can_delete=False,
                                            extra=total)
    # QuestionFormSetSubjective = formset_factory(SubjectiveQuestionAdd, can_delete=False, extra=subTotal)
    formset = QuestionFormSet(queryset=Question.objects.none(), instance=getObjectiveNum)
    # subjectiveForm = QuestionFormSetSubjective()
    if request.method == 'POST' and total > 0:
        formset = QuestionFormSet(request.POST, instance=getObjectiveNum)
        if formset.is_valid():
            formset.instance.exam_id = getObjectiveNum
            formset.save(commit=True)
            addNotificationNewExam(examId)
            # if request.method == 'POST' and subTotal>0:
            #     subjectiveForm = QuestionFormSetSubjective(request.POST, instance=getSubjectiveNum)
            #     if subjectiveForm.is_valid():
            #         subjectiveForm.instance.exam_id = getSubjectiveNum
            # subjectiveForm.save(commit=True)
            return redirect('teacherExamList')
    notification = Notification.objects.all().filter(user_type='Teacher')

    return render(request, 'manageExamContent.html', {'formset': formset, 'examId': examId, 'totalObjectiveQue': total,
                                                      'notification':notification})


@login_required(login_url='index')
@check_teacher_authentication
def setExamInfo(request, exam_id):
    exams = Examination.objects.get(examId=exam_id)
    exam_form = editExamTeacherForm(instance=exams)

    if request.method == 'POST':
        print('here')
        exam_form = editExamTeacherForm(request.POST, instance=exams)
        if exam_form.is_valid():
            exam_form.save()
            exam_id = exam_id
            allFieldsExam = Examination.objects.all().filter(examId=exam_id)
            total_objective = request.POST.get('totalObjectiveQues')
            val = int_or_0(exam_id)
            objective_ques_num = int_or_0(total_objective)
            print("**********************", total_objective)
            addNotificationNewExamTeacher(exam_id)
            # for i in "x"|ljust:totalObjectiveQue:
            #     addExamContentOnlyIdObjective(exams)
            return redirect('../manageExamContent/' + exam_id)
        else:
            print('error')
    context = {'form': exam_form}
    return render(request, 'setExamInfoTeacher.html', context)


@login_required(login_url='index')
@check_super_user
def manageCourse(request):
    return render(request, 'manageCourse.html')


@login_required(login_url='index')
@check_super_user
def form_add_exam(request):
    form = forms.ExaminationAdd()
    exams = Examination.objects.all()
    exam_text = 'Add Examination'
    add_type = 'Add'
    myFilter = ExamFilter(request.POST, queryset=exams)
    exams = myFilter.qs
    if request.method == 'POST':
        if 'addExam' in request.POST:
            form = forms.ExaminationAdd(request.POST)
            try:
                form.save(commit=True)
                exam = Examination.objects.latest('examId')
                addNotificationNewExamTeacher(exam.examId)
                messages.success(request, 'Examination successfully added!')
                return redirect('../manageExam')
            except Exception as e:
                messages.error(request, 'Please enter valid information!')
                return redirect('../manageExam')
        if 'searchExam' in request.POST:
            exams = myFilter.qs
    notification = Notification.objects.all().filter().order_by('-id')
    return render(request, 'manageExam.html', {'form': form,
                                               'exam_dict': exams,
                                               'exam_text': exam_text,
                                               'add_type': add_type,
                                               'myFilter':myFilter,
                                               'notification': notification})

@login_required(login_url='index')
@check_super_user
def update_exam(request, exam_id):
    exams = Examination.objects.get(examId=exam_id)
    exam_info = Examination.objects.all()
    exam_form = ExaminationAdd(instance=exams)
    exam_text = 'Edit Examination'
    error_message = ''
    success_message = ''
    add_type = 'Update'
    if request.method == 'POST':
        exam_form = ExaminationAdd(request.POST, instance=exams)
        if exam_form.is_valid():
            exam_form.save()
            messages.success(request, 'Examination successfully added!')
            return redirect('../manageExam')
        else:
            messages.error(request, 'Please enter valid information!')
            return redirect('../manageExam')
    return render(request, 'manageExam.html', {'form': exam_form,
                                               'exam_dict': exam_info,
                                               'exam_text': exam_text,
                                               'add_type': add_type,
                                               'success_message': success_message,
                                               'error_message': error_message
                                               })


def delete_exam(request,exam_id):
    exams = Examination.objects.get(examId=exam_id)
    exams.delete()
    messages.success(request, 'Exam deleted successfully!')
    return redirect('../manageExam')


@login_required(login_url='index')
@check_super_user
def form_add_course(request):
    courseList = Course.objects.all()
    course_dict = {'course': courseList}
    newCourseAdded = False
    course_form = forms.CourseForm()

    if request.method == 'POST':
        course_form = CourseForm(data=request.POST)
        try:
            course_form.save()
            newCourseAdded = True
            messages.success(request, 'Course Added Successfully!')
            return redirect('manageCourse')
        except Exception as e:
            messages.error(request, 'Please add a course with a unique course code!')
            return redirect('manageCourse')
    else:
        courseForm = CourseForm()
    notification = Notification.objects.all().order_by('-id')
    return render(request, 'manageCourse.html',
                  {'course_form': course_form, 'newCourseAdded': newCourseAdded, 'course_dict': courseList,'notification':notification})


@login_required(login_url='index')
def updateCourse(request, pk):
    courseList = Course.objects.all()
    courses = Course.objects.get(course_id=pk)
    course_form = CourseForm(instance=courses)
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=courses)
        if course_form.is_valid():
            course_form.save()
            # messages.success(request,'Course Added Successfully!')
            messages.success(request, 'Course Successfully Updated!')
            return redirect('manageCourse')
    context = {'course_form': course_form}
    return render(request, 'manageCourse.html', {'course_form': course_form,'course_dict':courseList})


@login_required(login_url='index')
@check_super_user
def deleteCourse(request, pk):
    success_message = ''
    error_message = ''
    courses = Course.objects.all().filter(course_id=pk)
    try:
        courses.delete()
        messages.success(request, 'Course Successfully Deleted!')
        return redirect('manageCourse')
    except ProtectedError:
        messages.error(request, 'Cannot delete a course with examinations related to it!')
        return redirect('manageCourse')
        #error_message = 'Cannot delete a course with examinations related to it!'
        #print('**********Error**********')
    #return render(request, 'manageCourse.html', {'success_message': success_message, 'error_message': error_message})


@login_required(login_url='index')
def setQues_view(request):
    examList = Examination.objects.all()
    exam_dict = {'exam': examList}
    return


@login_required(login_url='index')
@check_super_user
def teacherListView(request):
    teacherList = UserProfileInfo.objects.all().filter(userType="Teacher")
    myFilter = StudentFilter(request.POST, queryset=teacherList)
    teacherList = myFilter.qs
    notification = Notification.objects.all().order_by('-id')
    return render(request, 'teacherList.html', {'teacher_dict': teacherList,'myFilter':myFilter,'notification':notification})


@login_required(login_url='index')
@check_teacher_authentication
def examListView(request):
    user = User.objects.all().filter(username=request.user)
    userinfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = userinfo.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher').order_by('-id')
    examList = Examination.objects.all().filter(~Q(exam_status='Expired'), course_code=getCourse)
    # if examList.count() > 0:
    checkExamStatus(request)
    return render(request, 'teacherExamList.html', {'exam_dict': examList,'notification':notification})


@login_required(login_url='index')
@check_student_authentication
def examListViewStudent(request):
    checkExamStatus(request)
    users = User.objects.all().filter(username=request.user)
    getInfo = UserProfileInfo.objects.all().filter(user__in=users).first()
    course = getInfo.course_id
    attendance = ExamAttendance.objects.all().filter(student_id=getInfo).values('exam_id')
    examList = Examination.objects.all().filter(exam_status='Live', course_code=course)
    student_id = UserProfileInfo.objects.all().filter(user__in=users).first()
    getCourse = student_id.course_id
    notification = Notification.objects.all().filter(course_id = getCourse).order_by('-id')
    exam_list = ExamAttendance.objects.all().filter(student_id= getInfo)
    exam_dict = {'exam': examList}
    return render(request, 'studentExamList.html', {'exam_dict': examList,'attendace_list':attendance,'notification': notification})


@login_required(login_url='index')
def form_name_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            return adminDashboard(request)
    return render(request, 'login.html', {'form': form})


@login_required(login_url='index')
@check_super_user
def addDashBoardInfoAdmin(request):
    course_list = Course.objects.all().count()
    print('Heyyyyyyyyyy', course_list)
    return render(request, 'adminDashboard00.html', {'course_list': course_list})





def calculate_grade(obtainedMarks, finalMarks):
    grade = ''
    if (obtainedMarks / finalMarks) * 100 >= 70:
        grade = 'A'
    elif (obtainedMarks / finalMarks) * 100 >= 55:
        grade = 'B'
    elif (obtainedMarks / finalMarks) * 100 >= 45:
        grade = 'C'
    elif (obtainedMarks / finalMarks) * 100 >= 40:
        grade = 'D'
    elif (obtainedMarks / finalMarks) * 100<40:
        grade = 'F'
    return grade

# to calculate the total marks and store
def calculate_final_marks(request, examId):
    result = FinalResult()
    exam_info = Examination.objects.all().filter(examId=examId).first()
    user = User.objects.all().filter(username=request.user)
    student_info = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCalculatedMarks = CalculatedMark.objects.all().filter(exam_id=exam_info, student_id=student_info)
    #get the total sum
    getSum = getCalculatedMarks.aggregate(sum=Sum('total_weight'))['sum']
    #get the grade
    getGrade = calculate_grade(getSum, exam_info.totalMarks)
    #add records of final result
    FinalResult.objects.update_or_create(
        exam_id=exam_info, student_id=student_info,
        defaults={'total_marks_obtained':getSum, 'grade':getGrade}
    )

def calculate_marks(request, exam_id, question_id, answer):
    #get the exam and user information
    exam_info = Examination.objects.all().filter(examId=exam_id).first()
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    #get the question
    question = Question.objects.all().filter(id=question_id).first()
    original_answer = question.answer
    total_marks = question.total_marks
    #check if the user's answer and the correct answer matches
    if to_str(original_answer) == to_str(answer):
        #if answers match store the questions total weight
        getMark = total_marks
    else:
        # else store zero
        getMark = 0
    #store the marks for the question, student and examination
    CalculatedMark.objects.update_or_create(
        exam_id=exam_info, student_id=student_id,question_id=question,
        defaults={'obj_answer':answer, 'total_weight':getMark}
    )


def makeExamExpire(request,exam_id):
    Examination.objects.all().filter(examId=exam_id).update(exam_status='Expired')
    return redirect('expiredExams')


# make submitted
def attendanceUpdateStatusExam(request, examId):
    #get user and exam information
    exam_val = Examination.objects.all().filter(examId=examId).first()
    getExam = Examination.objects.get(examId=examId)
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    # if time has already exceeded save as late submission
    if utc2local(getExam.exam_end_time) < datetime.datetime.now().replace(tzinfo=utc):
        #set as late submission
        ExamAttendance.objects.all().filter(exam_id=exam_val, student_id=student_id).update(
            exam_status='Late Submission')
    else:
        #set as normal submission
        ExamAttendance.objects.all().filter(exam_id=exam_val, student_id=student_id).update(
            exam_status='Exam Submitted')


@login_required(login_url='index')
def giveExam(request, examId):
    exam_val = Examination.objects.all().filter(examId=examId).first()
    exam_id = Examination.objects.all().filter(examId__in=examId).first()
    getVal = Examination.objects.get(examId=examId)
    exam_end_time = getVal.exam_end_time
    print('exam_id...',examId)
    question = Question.objects.all().filter(exam_id=exam_val)
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    my_list = list(question)
    shuffle(my_list)
    counter=0
    if request.method=='POST':
        ques = request.POST.getlist('ques_id')
        answer = request.POST.getlist('answerSelect')
        for i in question:
            Response.objects.update_or_create(
                exam_id=exam_val, student_id=student_id, question_id=question[counter],
                defaults={"obj_answer": answer[counter]},
            )
            attendanceUpdateStatusExam(request,getVal.examId)
            ques = question[counter]
            ans = answer[counter]
            calculate_marks(request,examId,ques.id,answer[counter])
            calculate_final_marks(request, examId)
            counter= counter+1
        messages.success(request, 'Successfully submitted exam!')
        return redirect('../../studentExamList')
    return render(request, 'giveExam.html', {'question': question,'exam_end_time':exam_end_time})


# makes started
def attendanceStatusExam(request, examId):
    #get user and exam information
    exams = Examination.objects.all().filter(examId=examId).first()
    username = User.objects.all().filter(username=request.user).first()
    student_id = UserProfileInfo.objects.all().filter(user=username).first()
    #set exam status of student as started
    ExamAttendance.objects.update_or_create(
        exam_id=exams, student_id=student_id,
        defaults={'exam_status': "Exam Started"}
    )


def face_gen(camera, request):
    while True:
        try:
            frame = camera.get_frame(request.user, getExamId)
            if frame is None:
                return redirect('index')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except StopIteration:
            break
    return redirect('index')


def face_feed(request):
    return StreamingHttpResponse(face_gen(checkFace(), request),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


getExamId = 0

@login_required(login_url='index')
@check_student_authentication
def facialRecognition(request):
    face_feed(request)
    return render(request, 'faceDetection.html', {})


@login_required(login_url='index')
def authenticate_user(request, examId):
    global getExamId
    getExamId = examId
    print('Exam ID',getExamId)
    exams = Examination.objects.values_list('exam_pass', flat=True).get(examId=examId)
    exam_val = Examination.objects.get(examId=examId)
    # getVal = exams('')
    # my_list = list(exams)
    form = forms.addExamPass
    if request.POST:
        print('******************', exams)
        if check_password(request.POST.get('exam_pass'), exams):
            attendanceStatusExam(request, exam_val.examId)
            # return redirect('../giveExam/' + examId)
            facialRecognition(request)
            return redirect('facialRecognition')
        else:
            return redirect('../studentExamList')

    return render(request, 'authenticate.html', {'examId': examId, 'form': form})

#student
def addNotificationLiveExam(examId):
    exams = Examination.objects.all().filter(examId=examId).first()
    notification = Notification()
    notification.course_id = exams.course_code
    notification.notification_text = 'This is to notify you that your exam '+exams.examName+' is live now!'
    notification.user_type = 'Student'
    notification.save()

def makeExamLive(examId):
    exam_list = Examination.objects.all().filter(examId=examId).update(exam_status='Live')
    getCourse = Examination.objects.get(examId=examId)
    course = getCourse.course_code
    val_course = Course.objects.all().filter(course_name= course).first()
    elist = UserProfileInfo.objects.all().filter(course_id=val_course)
    users = UserProfileInfo.objects.values_list('user__email', flat=True).filter(course_id=val_course)
    emails = list(users)
    send_mail('Live Exam!','Your examination ' + getCourse.examName + ' of course ' + str(course) + ' is live now! Please give your examination on time.',
               'sagunrupakheti@gmail.com', emails, fail_silently=False)
    return True


def addExactTime(examId):
    exams = Examination.objects.get(examId=examId)
    total_time = exams.duration
    print('*******',datetime.timedelta(minutes=exams.duration))
    endTime = datetime.datetime.now()+ datetime.timedelta(minutes=exams.duration, seconds=0,hours=0,days=0)
    print('^^^^',endTime)
    updateExam = Examination.objects.all().filter(examId=examId).update(exam_end_time=endTime,
                                                                        exactTimeStart=datetime.datetime.now().time(),
                                                                        exam_date=datetime.date.today())
    return True

# def sendPasswordNotification(request,examId):
#     exams = Examination.objects.all().filter(examId=examId).first()
#     notification = Notification()
#     notification.course_id = exams.course_code
#     notification.notification_text = 'This is to notify you that the password for your exam is '+exams.examName+' on '+ str(exams.exam_date)
#     notification.user_type = 'Student'
#     notification.save()


@login_required(login_url='index')
@check_teacher_authentication
def showPasswordView(request, examId):
    form = forms.addExamPass
    exam = Examination.objects.all().filter(examId=examId).first()
    getExam = Examination.objects.get(examId=examId)
    print('^^^^^^',getExam.duration)
    if request.method == "POST":
        exam_list = Examination.objects.all().filter(examId=examId).update(
            exam_pass=make_password(request.POST.get('exam_pass')))
        makeExamLive(examId)
        addNotificationLiveExam(examId)
        addNotificationNewExamTeacher(examId)
        addExactTime(examId)
        messages.success(request, 'Successfully made examination live! The students have been sent an email and notification to notify!')
        return redirect('../teacherExamList')
    return render(request, 'examPasswordView.html', {'form': form})


# @login_required(login_url='index')
# @check_teacher_authentication
# to show all the expired exams list
def givenExams(request):
    user = User.objects.all().filter(username=request.user)
    userinfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = userinfo.course_id
    course = Course.objects.all().filter(course_name=getCourse).first()
    print(getCourse)
    exam = Examination.objects.all().filter(exam_status='Expired', course_code= getCourse)
    print(exam)
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher').order_by('-id')
    return render(request, 'viewGivenExamListTeacher.html', {'exam_dict': exam,'notification':notification})

# @login_required(login_url='index')
# @check_teacher_authentication
def manageResult(request, examId):
    getExam = Examination.objects.all().filter(examId= examId).first()
    gr = FinalResult.objects.all().filter(exam_id=getExam)
    status = ExamAttendance.objects.all().filter(exam_id=getExam,exam_status='Exam Submitted')|ExamAttendance.objects.all().filter(exam_id=getExam,exam_status='Late Submission')
    get_result = zip(gr,status)
    user = User.objects.all().filter(username=request.user)
    userinfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = userinfo.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher').order_by('-id')
    get_result_not_submit = ExamAttendance.objects.all().filter(exam_id=getExam,exam_status='Exam Started')
    not_submitted = zip(gr,get_result_not_submit)
    return render(request, 'manageResult.html', {'get_result': get_result,'notification':notification,'not_submitted':not_submitted})


@login_required(login_url='index')
@check_student_authentication
# show result to particular student
def showResultStudent(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    get_result = FinalResult.objects.all().filter(student_id=student_id, status='Live')
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = student_id.course_id
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Student').order_by('-id')
    return render(request, 'showResultStudent.html', {'get_result': get_result,'notification':notification})



# change from pending to live
def changeResultVisibility(request, id):
    exam_list = FinalResult.objects.all().filter(id=id).update(status='Live')
    getUser = FinalResult.objects.get(id=id)
    student = getUser.student_id
    exam = getUser.exam_id
    user = User.objects.get(username=student)
    getEmail = user.email
    send_mail('Live Result!', 'Your result is live now! Please review it and let us know if you have any problem.',
              'sagunrupakheti@gmail.com', [getEmail], fail_silently=False)
    messages.success(request, 'Successfully made result live!')
    return redirect('../manageResult/'+str(exam))


def changeResultVisibilityReverse(request, id):
    exam_list = FinalResult.objects.all().filter(id=id).update(status='Pending')
    return redirect('expiredExams')


# check if the user's pics have been clicked
def checkStatusCollectionPics(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    get_status = SamplePicsStatus.objects.all().filter(student_id=student_id).first()
    print(request.user)
    if get_status is not None:
        if get_status.collection_status == 'Collected':
            return True
    else:
        return False


# redirect after checking if pictures for dataset havve been clicked
def picsCollect(request):
    if checkStatusCollectionPics(request) == True:
        return redirect('../teacherDashboard00')
    else:
        return redirect('index')


def gen(camera, request):
    while True:
        # if checkStatusCollectionPics(request) == True:
        #     return redirect('index')
        try:
            userName = request.user
            print('Views ko user', request.user)
            frame = camera.get_frame(getReq)
            if frame is None:
                return redirect('index')
            else:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except StopIteration:
            break
    return redirect('index')


def gen2(camera):
    frame = camera.click_pic()
    if frame is None:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def click_pic(request):
    # gen(VideoCamera)
    # gen2((VideoCamera()))

    return StreamingHttpResponse(gen2(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def video_feed(request):
    # gen(VideoCamera)
    # gen2((VideoCamera()))
    # if checkStatusCollectionPics(request)==True:
    #     return  redirect('index')
    return StreamingHttpResponse(gen(VideoCamera(), request),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

# @login_required(login_url='index')
# show the face detection part
def showCamera(request):
    # if checkStatusCollectionPics(request) == True:
    #     return redirect('index')
    # try:
    # except Exception:
    #     return redirect('index')
    video_feed(request)
    return render(request, 'showCamera.html', {})

#check authentications
@login_required(login_url='index')
@check_student_authentication
def checkAuthenticateUser(request):
    #get current user information
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
    exam = Examination.objects.all().filter(examId = getExamId).first()
    #check if the user has been saved as authenticated
    get_status = AuthenticateExam.objects.all().filter(student_id=student_id,exam_id= exam).first()
    if get_status is not None:
        # if the user has been authenticated redirect to the examination page with questions
        if get_status.authenticate_status == 'Authenticated':
            return redirect ('../giveExam/' + str(getExamId))
        else:
            #else return to the page with facial recognition
            return redirect('facialRecognition')
    else:
        return redirect('facialRecognition')
    return render(request, 'faceDetection.html')


@login_required(login_url='index')
@check_teacher_authentication
def updatePasswordTeacher(request):
    errorMessage = ''
    if request.POST:
        if request.POST.get('firstPass') == request.POST.get('confirmPass'):
            changePass = User.objects.all().filter(username=request.user).update(
                password=make_password(request.POST.get('confirmPass')))
            return redirect('../teacherDashboard00')
        else:
            messages.error(request, 'Both passwords do not match!')
            return redirect('updatePasswordTeacher')
    return render(request, 'updatePasswordTeacher.html', {'errorMessage': errorMessage})

# @login_required(login_url='index')
def updatePasswordStudent(request):
    errorMessage = ''
    if request.POST:
        if request.POST.get('firstPass') == request.POST.get('confirmPass'):
            User.objects.all().filter(username=request.user).update(
                password=make_password(request.POST.get('confirmPass'))) #update password
            return HttpResponseRedirect('showCamera') #send to image collection
        else:
            messages.error(request, 'Both passwords do not match!')
            return redirect('updatePasswordStudent')
    return render(request, 'updatePasswordStudent.html', {'errorMessage': errorMessage})


def redirectToDashboard():
    return redirect('../studentDashboard00')

@login_required(login_url='index')
@check_student_authentication
def send_profile_info_student(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user)
    teach = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = teach.course_id
    useInfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    form = UserProfileUpdatePic
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Student').order_by('-id')
    if request.method == "POST":
        if ('profile_pic' in request.FILES):
            editForm = UserProfileUpdatePic(request.POST,request.FILES,instance=useInfo)
        try:
            editForm.save()
            messages.success(request, 'Successfully updated profile picture!')
            return redirect('../student_info')
        except Exception:
            messages.error(request, 'Could not update your profile picture!')
            return redirect('../student_info')
    return render(request,'showUserProfileStudent.html',{'user_info':student_id,'form':form,'notification':notification})

@login_required(login_url='index')
@check_teacher_authentication
def send_profile_info_teacher(request):
    user = User.objects.all().filter(username=request.user)
    teacher_id = UserProfileInfo.objects.all().filter(user__in=user)
    teach = UserProfileInfo.objects.all().filter(user__in=user).first()
    getCourse = teach.course_id
    useInfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    form = UserProfileUpdatePic
    notification = Notification.objects.all().filter(course_id=getCourse, user_type='Teacher').order_by('-id')
    if request.method == "POST":
        if ('profile_pic' in request.FILES):
            editForm = UserProfileUpdatePic(request.POST,request.FILES,instance=useInfo)
        try:
            editForm.save()
            messages.success(request, 'Successfully updated profile picture!')
            return redirect('../teacher_info')
        except Exception:
            messages.error(request, 'Could not update your profile picture!')
            return redirect('../teacher_info')
    return render(request, 'showUserProfileTeacher.html', {'user_info': teacher_id,'notification':notification,'form':form})

@login_required(login_url='index')
@check_super_user
def send_profile_info_admin(request):
    user = User.objects.all().filter(username=request.user)
    student_id = UserProfileInfo.objects.all().filter(user__in=user)
    useInfo = UserProfileInfo.objects.all().filter(user__in=user).first()
    form = UserProfileUpdatePic
    notification = Notification.objects.all().order_by('-id')
    if request.method == "POST":
        if ('profile_pic' in request.FILES):
            editForm = UserProfileUpdatePic(request.POST,request.FILES,instance=useInfo)
        try:
            editForm.save()
            messages.success(request, 'Successfully updated profile picture!')
        except Exception:
            messages.error(request, 'Could not update your profile picture!')
    return render(request,'showUserProfileAdmin.html',{'user_info':student_id,'notification':notification,'form':form})

def showPaperDetailsTeacher(request,exam_id,student_id):
    exam = Examination.objects.all().filter(examId= exam_id).first()
    ques = Question.objects.all().filter(exam_id=exam)
    user =User.objects.all().filter(username=student_id).first()
    user_info = UserProfileInfo.objects.all().filter(user=user).first()
    u = UserProfileInfo.objects.get(user=user)
    temp = ''
    if u.userType == 'Teacher':
        temp = 'teacherDashboard.html'
    elif u.userType == 'Student':
        temp = 'studentDashboard.html'

    e= Examination.objects.get(examId= exam_id)
    fname = u.firstName + ' ' +u.lastName
    total = e.totalMarks
    course = e.course_code
    exam_name = e.examName
    response = Response.objects.all().filter(exam_id=exam,student_id=user_info)
    finalResult = FinalResult.objects.get(exam_id=exam,student_id=user_info)
    marks = finalResult.total_marks_obtained
    grade = finalResult.grade
    question = zip(ques, response)

    print(ques)
    return render(request,'viewStudentPaper.html',{'question':question,'fname':fname,'course':course,'examName':exam_name,'total':total,
                                                   'marks':marks,'temp':temp,'grade':grade})



def help(request):
    my_new_dict = {'help_dict': 'I am help from views'}
    return render(request, 'help.html', context=my_new_dict)

def error(request):
    return render(request,'404error.html')


