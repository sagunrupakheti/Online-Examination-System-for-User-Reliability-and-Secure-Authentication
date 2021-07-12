from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from first_app.models import AccessRecord, Topic, Webpage, Examination, UserProfileInfo, Course, Teacher, Student, Question, \
    Response, CalculatedMark, FinalResult, ExamAttendance,SamplePicsStatus,AuthenticateExam, Notification
import json

class TestViews(TestCase):
    def setUp(self):
        self.client= Client()
        self.index_url = reverse('index')
        self.login_url = reverse('login')


    def test_index_GET(self):
        client = Client()
        response = client.get(self.index_url)
        #if it works correctly
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

    def test_login_POST(self):
        user = User.objects.create(username='sagun',password='asdfg')
        response = self.client.post(self.login_url,username='sagun',passwordooo='asdfg')
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')