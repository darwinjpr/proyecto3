#Import necesary libraries
import cv2
import pickle
import face_recognition
import numpy as np
from datetime import date, datetime, timedelta

#Function for headline
def headline():
	file = open("Informe.txt","a+")
	file.write("Lista de intrusiones detectadas\n\n")
	file.close()
	return 0

#Function for report
def report(momento,tipo,contador):
	file = open("Informe.txt","a+")
	
	file.write("Numero de deteccion: {}\n".format(contador))
	file.write("Persona detectada: "+tipo+"\n")
	file.write("Fecha: {}/{}/{}\n".format(momento.day, momento.month, momento.year))
	file.write("Hora: {}:{}\n".format(momento.hour, momento.minute))
	
	file.close()
	return contador + 1

#Function for duration report
def timecounter(duration):
	file = open("Informe.txt","a+")
	file.write("Duracion: {}:{}\n".format(duration.minute, duration.second))
	file.write("\n------------------\n\n")
	file.close()
	return 0

#Function for recognize faces in the picture
def recognizer(frame,encoding,matches):
	#Reformat frame
	RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	
	#Find faces in the image
	boxes = face_recognition.face_locations(RGB, model="hog")
	encodings = face_recognition.face_encodings(RGB, boxes)
	
	for encoding in encodings:
		matches = face_recognition.compare_faces(np.array(encoding),np.array(data["encodings"]))
	
	if True in matches:
		return "Edwin"
	else:
		return "Desconocida"

#Global variables
cont = 1
First = True
Registered = False
Intrusion = False
now = datetime.now()
reference = datetime.now()
end = datetime.now()
start = datetime.now()
encoding = "./modelo.pickle"
data = pickle.loads(open(encoding,"rb").read())
matches = [False]

#Writes headline
headline()

#Capture video from webcam
cap = cv2.VideoCapture(0)

#Writes the output in the footage.avi file
out = cv2.VideoWriter('footage.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15.0, (640,480))

#Captures two frames from the webcam video
_, frame = cap.read()
_, postframe = cap.read()

while (True):

	#Resize frames
	frame = cv2.resize(frame, (640,480))
	postframe = cv2.resize(postframe, (640,480))
	
	#Capture movement in the video
	diff = cv2.absdiff(frame, postframe)
	
	#Reformat video for better performance
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5,5), 0)
	_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
	
	#Creates the contours
	_, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	#Detect motion based on contours
	for contour in contours:
		if cv2.contourArea(contour) > 400:
			#Save video
			out.write(frame.astype('uint8'))
			
			now = datetime.now()
			end = now + timedelta(seconds=3)
			
			Intrusion = True
			break
			
	#Checks if it is a new intrusion
	if First and Intrusion:
		First = False
		reference = now + timedelta(seconds=3)
		start = datetime.now()

	elif now >= reference and not Registered and Intrusion:
		Registered = True
		#Write report
		person = recognizer(frame,encoding,matches)
		cont = report(now,person,cont)
	
	#Checks moment of last detected movement
	now2 = datetime.now()
	if now2 >= end and not First:
		duration = now2 - start - timedelta(seconds=3)
		duration = duration - timedelta(microseconds=duration.microseconds)
		duration = datetime.strptime(str(duration), "%H:%M:%S")
		timecounter(duration)
		First = True
		Registered = False

	#Only for debugging purposes (normally commented)
	cv2.imshow("Frame", frame)
	
	#Captures the next frames
	frame = postframe
	_, postframe = cap.read()
	
	#Ends the program
	key = cv2.waitKey(1)
	if key == 27: break
	
	Intrusion = False

cap.release()
out.release()
cv2.destroyAllWindows()
