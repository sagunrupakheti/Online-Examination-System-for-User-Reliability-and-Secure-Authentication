from django import forms
from django.core import validators
from .models import Examination, UserProfileInfo, Course, Teacher, Question, Response
from django.contrib.auth.models import User
import datetime
from datetime import date

class UserForm(forms.ModelForm):
    # for password
    # password = forms.CharField(widget=forms.PasswordInput())
    # defines how userform class behaves
    class Meta():
        model = User
        fields = ('username', 'email','password')
        help_texts = {
            'username': None,
        }
        label = ""
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','name': 'pass', 'id': 'pass'})
        }


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        CHOICES = (('Teacher', 'Teacher'), ('Student', 'Student'),)
        fields = ('firstName', 'lastName', 'dob', 'userType', 'contact', 'address','course_id', 'profile_pic')
        # labels = {
        # 'firstName' : " ",
        # 'lastName' : " "
        # }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker1'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'userType': forms.Select(choices=CHOICES, attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'course_id':forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

        def clean_date(self):
            dob = self.cleaned_data['dob']
            if dob > date.today():
                raise forms.ValidationError("The date cannot be in the future!")
            return dob

class UserProfileUpdatePic(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        exclude = ['firstName', 'lastName', 'dob', 'userType', 'contact', 'address','course_id',]
        fields={'profile_pic',}
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }
        def clean_date(self):
            dob = self.cleaned_data['profile_pic']

# def check_for_invalidName(value):
#     if value[0].lower() != 'sagun':
#         raise forms.ValidationError("Please input a valid name")
#
#
# def check_for_invalidPass(value):
#     if value[0] == 'letmein':
#         raise forms.ValidationError("Please input valid password")


class FormName(forms.Form):
    UserName = forms.CharField()
    Password = forms.CharField()
    # email = forms.EmailField()
    # verify_email = forms.EmailField(label="Enter your email again")
    # catch bots through inspect
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])
    checkName = 'sagun'

    def clean(self):
        all_clean_data = super().clean()
        name = all_clean_data['UserName']
        verifyName = 'sagun'
        password = all_clean_data['Password']

        if name != verifyName:
            raise forms.ValidationError("Please enter correct username")
        if password != 'letmein':
            raise forms.ValidationError("Please input valid password")


# class NewUser(forms.ModelForm):
#
#     class Meta():
#         model = allUser
#         fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta():
        model = Course
        fields = ('course_code', 'course_name')
        widgets = {
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class ExaminationAdd(forms.ModelForm):
    class Meta():
        model = Examination
        fields = ('course_code', 'examName', 'duration', 'exam_date')
        # course_code = forms.CharField()
        widgets = {
            'course_code': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}),
            'examName': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total time in minutes'}),
            'exam_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control timepicker'}),
        }

class addExamPass(forms.ModelForm):
    class Meta():
        model = Examination
        fields = ('exam_pass',)
        labels= {'exam_pass' : "Examination Password"}
        widgets = {
            'exam_pass': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class QuestionAdd(forms.ModelForm):
    class Meta():
        model = Question
        CHOICES = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
        fields = (
             'total_marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer')
        widgets = {

            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Question Weightage',
                                                    'name': 'totalMarks', 'id':'total'}),
            'question': forms.TextInput(attrs={'class': 'form-control', 'name': 'question', 'id': 'question'}),
            'option1': forms.TextInput(attrs={'class': 'form-control', 'name': 'option1', 'id': 'option1'}),
            'option2': forms.TextInput(attrs={'class': 'form-control', 'name': 'option2', 'id': 'option2'}),
            'option3': forms.TextInput(attrs={'class': 'form-control', 'name': 'option3', 'id': 'option3'}),
            'option4': forms.TextInput(attrs={'class': 'form-control', 'name': 'option4', 'id': 'option4'}),
            'answer': forms.Select(choices=CHOICES, attrs={'class': 'form-control', 'name': 'answer', 'id': 'answer'}),
        }

class SubjectiveQuestionAdd(forms.ModelForm):
    class Meta():
        model = Question
        fields = (
            'total_marks', 'question_no', 'question')
        widgets = {

            'total_marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Question Weightage',
                                                    'name': 'totalMarks', 'id':'total'}),
            'question_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Question Number',
                                                    'name': 'question_no', 'id': 'questionNo'}),
            'question': forms.TextInput(attrs={'class': 'form-control', 'name': 'question', 'id': 'question'}),
        }


class manageTeacherForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ('teacher_id', 'course_id')
        widgets = {
            'teacher_id': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}),
            'course_id': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Course'}),
        }


class editExamTeacherForm(forms.ModelForm):
    class Meta():
        model = Examination
        fields = ('totalObjectiveQues', 'exactTimeStart', 'totalMarks', 'passMarks','exam_pass')
        labels = {'exam_pass': "Examination Password",'totalObjectiveQues':"Total Questions",'exactTimeStart': "Time to start",
                  'totalMarks':"Total Marks", 'passMarks': "Pass Marks"}
        widgets = {
            'totalObjectiveQues': forms.NumberInput(attrs={'class': 'form-control'}),
            'exactTimeStart': forms.DateInput(attrs={'type': 'time', 'class': 'form-control timepicker'}),
            'totalMarks': forms.NumberInput(attrs={'class': 'form-control'}),
            'passMarks': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_pass': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'exam_pass'}),
        }

class showQuestionsStudentExam(forms.ModelForm):
    class Meta():
        model = Question
        # question = Question.objects.all().filter(id=id)
        fields = {'question','option1','option2','option3','option4','answer'}
        # label = {'question':" ",'option1':" ",'option2':" ",'option3':" ",'option4':" ",}
        CHOICES = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control border-0', 'name': 'question', 'id': 'question'}),
            'option1': forms.TextInput(attrs={'class': 'form-control border-0', 'name': 'option1', 'id': 'option1'}),
            'option2': forms.TextInput(attrs={'class': 'form-control border-0', 'name': 'option2', 'id': 'option2'}),
            'option3': forms.TextInput(attrs={'class': 'form-control border-0', 'name': 'option3', 'id': 'option3'}),
            'option4': forms.TextInput(attrs={'class': 'form-control border-0', 'name': 'option4', 'id': 'option4'}),
            'answer': forms.Select(choices=CHOICES, attrs={'class': 'form-control', 'name': 'answer', 'id': 'answer'}),
        }

class responseForm(forms.ModelForm):
    class Meta():
        model = Response
        fields= {'student_id','exam_id','question_id','obj_answer','sub_answer'}
        widgets={
            'student_id': forms.Select(),
            'exam_id': forms.Select(),
            'question_id': forms.Select(),
            'obj_answer': forms.TextInput(),
            'sub_answer': forms.TextInput(),
        }
