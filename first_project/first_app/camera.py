from io import BytesIO

import cv2,os,urllib.request
import numpy as np
from PIL import Image
from django.conf import settings
from . import models
from . import views
from .models import User, UserProfileInfo, SamplePicsStatus
import subprocess

face_detection_videocam = cv2.CascadeClassifier(os.path.join(settings.BASE_DIR,'opencv/haarcascade_frontalface_default.xml'))
count =0

# asd= (next(walk('../dataset')))
# if os.path.isdir('../dataset'):
#     print('DIR found')
paths = ('dataset')
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("opencv/haarcascade_frontalface_default.xml")
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    def __del__(self):
        self.video.release()

    def getImagesAndLabels(self):
        path = paths
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        print(imagePaths)
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')  # grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

        print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(self)
        recognizer.train(faces, np.array(ids))
        # Save the model into trainer/trainer.yml
        recognizer.write('try_trainer.yml')
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

    def get_frame(self,request):
        userInfo = User.objects.get(username=request)
        user = User.objects.all().filter(username=request)
        student_id = UserProfileInfo.objects.all().filter(user__in=user).first() #get the id of the current user
        global count
        count = count+1
        # status byte data
        success, image= self.video.read()
        #change to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #detect the face
        all_faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors= 5) #using haarcascade
        for (x, y, w, h) in all_faces_detected:#x coordinate, y- corrdinate, width and height of live video
            cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)#draw a rectangle around the face
            #save the images with their user id
            cv2.imwrite('dataset/User.'+str(userInfo.id)+'.'+ str(count)+'.jpeg', gray[y:y+h,x:x+w], [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            if count >= 30:  # Take 30 face sample and stop video
                count=0
                subprocess.call(['python', 'face_training.py']) #train the collected face data
                collection_status_pics = SamplePicsStatus() #add status as collected in the samplepicsstatus model
                collection_status_pics.student_id= student_id
                collection_status_pics.collection_status= 'Collected'
                collection_status_pics.save()
                return
                cv2.destroyAllWindows() #stop the live video making the video freeze
            break
        ret, jpeg = cv2.imencode('.jpg', image) #converts the image data into live streaming data, compresses images
        return jpeg.tobytes()
        cv2.destroyAllWindows()





    # class IPWebCam(object):
    #     def __init__(self):
    #         self.url = "http://192.168.0.100:8080/shot.jpg"
    #
    #     def __del__(self):
    #         cv2.destroyAllWindows()
    #
    #     def get_frame(self):
    #         imgResp = urllib.request.urlopen(self.url)
    #         imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    #         img = cv2.imdecode(imgNp, -1)
    #         # We are using Motion JPEG, but OpenCV defaults to capture raw images,
    #         # so we must encode it into JPEG in order to correctly display the
    #         # video stream
    #         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    #
    #         #draw rectangle around faces
    #         for (x, y, w, h) in faces_detected:
    #             cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
    #         resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)
    #         frame_flip = cv2.flip(resize, 1)
    #         ret, jpeg = cv2.imencode('.jpg', frame_flip)
    #         return jpeg.tobytes()