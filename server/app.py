import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import numpy as np
import json
from PIL import Image
import uuid
from flask_cors import CORS
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
import requests
import io
import traceback
load_dotenv()


app = Flask(__name__)
CORS(app)

face_client = FaceClient(os.getenv("END_POINT"), CognitiveServicesCredentials(os.getenv("API_KEY")))
PERSON_GROUP_ID = os.getenv("PERSON_GROUP")

@app.route("/login",methods=['POST'])
def login():
    username = request.get_json()['username']
    imageData = request.get_json()['imageData']
    img = Image.fromarray(np.array(list(imageData.values()),dtype="uint8").reshape(300,300,3))
    fname = f"temp/{str(uuid.uuid4())}.png"
    img.save(fname, format='PNG')
    img_stream = open(fname, "rb")
    sufficientQuality = True
    detected_faces = face_client.face.detect_with_stream(img_stream, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
    face_ids = []
    for face in detected_faces:
        if face.face_attributes.quality_for_recognition == QualityForRecognition.low:
            sufficientQuality = False
            os.remove(fname)
        else:
            face_ids.append(face.face_id)
    if len(face_ids) == 0:
        return jsonify({"success":False,"username":None,"message":"No Face Detected"})
    results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
    if not results:
        return jsonify({"success":False,"username":None,"message":"Face Not Recognized"})
    for person in results:
        if person.candidates:
            for candidate in person.candidates:
                if candidate.confidence > 0.5:
                    person = face_client.person_group_person.get(PERSON_GROUP_ID, candidate.person_id)
                    if person.name == username:
                        os.remove(fname)
                        return jsonify({"success":True,"username":person.name,"message":"Login Sucessful"})
    return jsonify({"sucess":False,"username":None,"message":"Login not sucessful"})

@app.route("/signup",methods=['POST'])
def signup():
    fname = f"temp/{str(uuid.uuid4())}.png"
    try:
        username = request.get_json()['username']
        imageData = request.get_json()['imageData']
        img = Image.fromarray(np.array(list(imageData.values()),dtype="uint8").reshape(300,300,3))
        img.save(fname, format='PNG')
        img_stream = open(fname, "r+b")
        sufficientQuality = True
        detected_faces = face_client.face.detect_with_stream(img_stream, detection_model='detection_03', recognition_model='recognition_04', return_face_attributes=['qualityForRecognition'])
        face_ids = []
        for face in detected_faces:
            face_ids.append(face.face_id)
            if face.face_attributes.quality_for_recognition == QualityForRecognition.low:
                sufficientQuality = False
                os.remove(fname)
                return  jsonify({"success":False,"person_id":None,"message":"Low Quality Image"})
        if len(face_ids) == 0:
            return jsonify({"success":False,"person_id":None,"message":"No Face Detected"})
        img_stream.seek(0)
        user = face_client.person_group_person.create(PERSON_GROUP_ID, username)
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, user.person_id, img_stream)
        # Train the person group
        face_client.person_group.train(PERSON_GROUP_ID)
        img_stream.close()
        os.remove(fname)
        return jsonify({"success":True,"person_id":user.person_id,"message":"User Created"})
    except Exception as e:
        traceback.print_exc()
        os.remove(fname)
        return jsonify({"success":False,"person_id":None,"message":str(e)})


if __name__ == "__main__":
    app.run(port=5000, debug=True)