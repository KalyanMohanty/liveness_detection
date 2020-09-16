# liveness_detection
│   gather.bat
│   gather_examples.py
│   le.pickle
│   liveness.model
│   liveness_demo.py
│   runLiveness.bat
│   trainLiveness.bat
│   train_liveness.py
│   webcam.bat
│   webcam.py
│
├───dataset
│   ├───fake
│   └───real
├───face_detector
│       deploy.prototxt
│       res10_300x300_ssd_iter_140000.caffemodel
│
├───pyimagesearch
│   │   livenessnet.py
│   │   __init__.py
│   │
│   └───__pycache__
│
└───videos

command to run code
python liveness_demo.py --model liveness.model --le le.pickle --detector face_detector

[![Watch the video]](https://youtu.be/-TL9wrp7KoY)

