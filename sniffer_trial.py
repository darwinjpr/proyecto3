#Import necesary libraries
import cv2
import numpy as np

#Function for fake repport
def fake_repport():
	file = open("Informe.txt","a+")
	file.write("Lista de intrusiones detectadas\n\n")
	file.write("Numero de deteccion: 1\n")
	file.write("Persona detectada: Desconocido\n")
	file.write("Fecha: 11/04/1998\n")
	file.write("Hora: 23:30\n")
	file.close()
	return 0

#Writes fake_repport
fake_repport()

#Capture video from webcam
cap = cv2.VideoCapture(0)

#Writes the output in the footage.avi file
out = cv2.VideoWriter('footage.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (640,480))

#Captures two frames from the webcam video
_, frame = cap.read()
_, postframe = cap.read()

while (True):
	try:
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
				break

		#Only for debugging purposes (normally commented)
		#cv2.imshow("Frame", frame)
		
		#Captures the next frames
		frame = postframe
		_, postframe = cap.read()
		
		#Ends the program
		key = cv2.waitKey(1)
		if key == 113: break

	except KeyboardInterrupt:
		break

cap.release()
out.release()
cv2.destroyAllWindows()