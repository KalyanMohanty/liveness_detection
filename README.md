# liveness_detection
[Watch the video](https://youtu.be/-TL9wrp7KoY)

## webcam.py
Captures the viedo form webcam
## gather_example.py
Gathers the face data of real and fake faces to the database
## train_liveness.py
To train the model on real and fake images
## liveness_demo.py
The python file runs with the help of arg pass
command to run code:

python liveness_demo.py --model liveness.model --le le.pickle --detector face_detector
## noargpass
The python file runs without the help of arg pass
## app.py
To run the application flask app in local
## app2.py
To access server the site camera 
1. Till now it able to capture the image from server site camera

![](Capture.PNG)



