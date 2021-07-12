from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date



class Course(models.Model):
    course_id = models.AutoField(primary_key=True, unique=True)
    course_code = models.CharField(max_length=8, unique=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Birth Date cannot be future date')


def no_past(value):
    today = date.today()
    if value < today or value == today:
        raise ValidationError('Exam Date cannot be past day')


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    firstName = models.CharField(max_length=255, blank=True)
    lastName = models.CharField(max_length=255, blank=True)
    userType = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    dob = models.DateField(auto_now_add=False, auto_now=False, blank=True, validators=[no_future])
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    # for printing the model
    def __str__(self):
        # default attribute of user
        return self.user.username


class Topic(models.Model):
    # for total characters
    top_name = models.CharField(max_length=264, unique=True)

    def __str__(self):
        return self.top_name


class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.DO_NOTHING, )
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.DO_NOTHING, )
    date = models.DateField()

    def __str__(self):
        return str(self.date)


# class allUser(models.Model):
#     userId = models.AutoField(primary_key=True)
#     firstName = models.CharField(max_length=255)
#     lastName = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     userType = models.CharField(max_length=255)
#     contact = models.CharField(max_length=255)

class Examination(models.Model):
    examId = models.AutoField(primary_key=True, unique=True)
    course_code = models.ForeignKey(Course, to_field='course_id', on_delete=models.PROTECT)
    examName = models.CharField(max_length=255)
    duration = models.IntegerField()
    exam_date = models.DateField(validators=[no_past])
    totalObjectiveQues = models.IntegerField(default=0, blank=True)
    totalSubjectiveQues = models.IntegerField(default=0, blank=True)
    exactTimeStart = models.TimeField(default=datetime.time(datetime.now()))
    totalMarks = models.IntegerField(default=0, blank=True)
    passMarks = models.IntegerField(default=0, blank=True)
    exam_status = models.CharField(max_length=10, default='Pending')
    exam_condition = models.CharField(max_length=10, default='Available')
    exam_pass = models.CharField(max_length=255, blank=True)
    exam_end_time = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.examId)


class Teacher(models.Model):
    teacher_id = models.ForeignKey(UserProfileInfo, on_delete=models.DO_NOTHING, )
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)


class Student(models.Model):
    student_id = models.ForeignKey(UserProfileInfo, on_delete=models.DO_NOTHING, )
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)


class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    exam_id = models.ForeignKey(Examination, on_delete=models.CASCADE,related_name="ques_exam")
    total_marks = models.PositiveIntegerField(default=0)
    question_no = models.TextField(max_length=500)
    question = models.CharField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    choose = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=10, choices=choose)


class Response(models.Model):
    id= models.AutoField(primary_key=True, unique=True)
    student_id= models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    exam_id= models.ForeignKey(Examination, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE,related_name="ques_id")
    obj_answer = models.CharField(max_length=255)
    sub_answer = models.TextField()

    def __str__(self):
        return str(self.id)

class CalculatedMark(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    exam_id= models.ForeignKey(Examination, on_delete=models.CASCADE)
    student_id= models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question,on_delete=models.CASCADE)
    obj_answer = models.CharField(max_length=255)
    total_weight = models.CharField(max_length=10, default=0)

class FinalResult(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student_id = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Examination, on_delete=models.CASCADE)
    total_marks_obtained = models.CharField(max_length=10)
    grade = models.CharField(max_length=5)
    status = models.CharField(max_length=10, default='Pending')

class ExamAttendance(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    student_id = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Examination, on_delete=models.CASCADE)
    exam_status = models.CharField(max_length=255)

class SamplePicsStatus(models.Model):
    student_id = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    collection_status = models.CharField(max_length=255)

class AuthenticateExam(models.Model):
    student_id = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Examination, on_delete=models.CASCADE)
    authenticate_status = models.CharField(max_length=255)

class Notification(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    course_id = models.ForeignKey(Course, to_field='course_id', on_delete=models.CASCADE)
    notification_text = models.TextField()
    user_type = models.CharField(max_length=255, default='Student')
    notification_date = models.DateField(default=datetime.now())