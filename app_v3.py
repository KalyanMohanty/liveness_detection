from flask import Flask, flash, redirect, render_template, \
     request, url_for,Response, jsonify, send_from_directory
from flask import redirect,url_for,session,logging,request
import os
import csv
import time
import json
import jsonify
import requests
import warnings
import datetime
import numpy as np
from flask import request
from flask import jsonify
from flask import Flask, render_template
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename

from imutils.video import VideoStream
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import argparse
import imutils
import pickle
import time
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/liveness',methods=['GET', 'POST'])
def liveness_detection():
	net = cv2.dnn.readNetFromCaffe("face_detector/deploy.prototxt", "face_detector/res10_300x300_ssd_iter_140000.caffemodel")

	print("[INFO] loading liveness detector...")
	model = load_model('liveness.model')
	le = pickle.loads(open('le.pickle','rb').read())

	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 600 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=600)
		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))
		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()
			# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]
			# filter out weak detections
			if confidence > 0.5:
				# compute the (x, y)-coordinates of the bounding box for
				# the face and extract the face ROI
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				# ensure the detected bounding box does fall outside the
				# dimensions of the frame
				startX = max(0, startX)
				startY = max(0, startY)
				endX = min(w, endX)
				endY = min(h, endY)
				# extract the face ROI and then preproces it in the exact
				# same manner as our training data
				face = frame[startY:endY, startX:endX]
				face = cv2.resize(face, (32, 32))
				face = face.astype("float") / 255.0
				face = img_to_array(face)
				face = np.expand_dims(face, axis=0)
				# pass the face ROI through the trained liveness detector
				# model to determine if the face is "real" or "fake"
				preds = model.predict(face)[0]
				j = np.argmax(preds)
				label = le.classes_[j]
				# draw the label and bounding box on the frame
				label = "{}: {:.4f}".format(label, preds[j])
				cv2.putText(frame, label, (startX, startY - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
			if request.method == 'POST':
				url = 'https://coeaifaceapi.herokuapp.com/face_rec'
				files = {'file': open('filename.jpg', 'rb')}
				resp = requests.post(url, files=files)
				#return json.dumps(resp.json(), skipkeys = True)
				print('Student name', resp)
			else:
				print('Fake persion detected')
		break
	ret, jpeg = cv2.imencode('.jpg',frame)
	return jpeg.tobytes()
		# show the output frame and wait for a key press
	# 	cv2.imshow("Frame", frame)
	# 	key = cv2.waitKey(1) & 0xFF
	# 	# if the `q` key was pressed, break from the loop
	# 	if key == ord("q"):
	# 		break
	# # do a bit of cleanup
	# cv2.destroyAllWindows()
	# vs.stop()
	#return 'correctly detected fake and real'
if __name__=='__main__':
	app.run(debug = True)
