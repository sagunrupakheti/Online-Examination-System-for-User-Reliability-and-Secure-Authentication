from django.test import SimpleTestCase
from django.urls import reverse
from django.urls import resolve
#from first_project import first_app
#from first_project.first_app.views import registerUser
from first_app.views import index, goLogin, user_logout, update_exam,adminDashboard,adminDashboard00,teacherDashboard,studentDashboard,\
    teacherDashboard00,studentDashboard00



class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, goLogin)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, user_logout)

    def test_adminDashboard_url_is_resolved(self):
        url = reverse('dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, adminDashboard)

    def test_adminDashboard_url_is_resolved(self):
        url = reverse('dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, adminDashboard)

    def test_adminDashboard00_url_is_resolved(self):
        url = reverse('dashboardx')
        print(resolve(url))
        self.assertEquals(resolve(url).func, adminDashboard00)

    def test_teacherDashboard_url_is_resolved(self):
        url = reverse('teacher_dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, teacherDashboard)

    def test_teacherDashboard00_url_is_resolved(self):
        url = reverse('teacher_dashboard00')
        print(resolve(url))
        self.assertEquals(resolve(url).func, teacherDashboard00)

    def test_studentDashboard_url_is_resolved(self):
        url = reverse('student_Dashboard')
        print(resolve(url))
        self.assertEquals(resolve(url).func, studentDashboard)

    def test_studentDashboard00_url_is_resolved(self):
        url = reverse('student_Dashboard00')
        print(resolve(url))
        self.assertEquals(resolve(url).func, studentDashboard00)

    def test_update_exam_url_is_resolved(self):
        url = reverse('updateExam', args=['str'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, update_exam)