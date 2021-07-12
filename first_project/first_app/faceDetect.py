from io import BytesIO

import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from django.http import request, HttpResponseRedirect

from . import views
from .models import User, UserProfileInfo, SamplePicsStatus, AuthenticateExam, Examination

# fetch_user_info = User.objects.all().values_list('username')
# print(list(fetch_user_info))

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(os.path.join(settings.BASE_DIR,"trainer.yml"))
cascadePath = (os.path.join(settings.BASE_DIR,"opencv/haarcascade_frontalface_default.xml"))
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
# iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
system_users = []
user_names = User.objects.values_list('username',flat=True)

names = ['None', 'Sagun', 'Shreyas','Rhicha','Rima','Kumar']
# Initialize and start realtime video capture
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height
# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
status = False

class checkFace(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def get_frame(self,request,examId):
        global status
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            exam = Examination.objects.all().filter(examId=examId).first()

            user = User.objects.all().filter(username=request)
            student_id = UserProfileInfo.objects.all().filter(user__in=user).first()
            # id = user_names[id]
            AuthenticateExam.objects.update_or_create(
                exam_id=exam,student_id=student_id,authenticate_status='Authenticated',defaults={"authenticate_status":'Authenticated'},
            )
            # If confidence is less them 100 ==> "0" : perfect match
            if (confidence < 100):
                if status == False:
                    print('asd')
                    status= True
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))


            cv2.putText(
                img,
                str(request),
                (x + 5, y - 5),
                font,
                1,
                (255, 255, 255),
                2
            )
        # Do a bit of cleanup
        # cam.release()
        cv2.destroyAllWindows()
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
