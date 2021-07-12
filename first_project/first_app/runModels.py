import subprocess

program_list = ['imageCapture.py', 'face_training.py','faceRecognition.py']

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)