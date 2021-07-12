from django.contrib import admin
from .models import AccessRecord, Topic, Webpage, Examination, UserProfileInfo, Course, Teacher, Student, Question, \
    Response, CalculatedMark, FinalResult, ExamAttendance,SamplePicsStatus,AuthenticateExam, Notification
# Register your models here.
admin.site.register(AccessRecord)
admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(Examination)
admin.site.register(UserProfileInfo)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(CalculatedMark)
admin.site.register(FinalResult)
admin.site.register(ExamAttendance)
admin.site.register(SamplePicsStatus)
admin.site.register(AuthenticateExam)
admin.site.register(Notification)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('course_id',)

admin.site.register(Course, CourseAdmin)
