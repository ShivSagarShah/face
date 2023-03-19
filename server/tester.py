# import os
# import json
# import requests
# import numpy as np
# from PIL import Image
# from dotenv import load_dotenv
# import uuid
# load_dotenv()
# from azure.cognitiveservices.vision.face import FaceClient
# from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
# import requests

# PERSON_GROUP_ID = str(uuid.uuid4())
# face_client = FaceClient(os.getenv("END_POINT"), CognitiveServicesCredentials(os.getenv("API_KEY")))
# # print('Person group:', PERSON_GROUP_ID)
# # face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name="btp_project", recognition_model='recognition_04')

# import numpy as np
# from PIL import Image
# import io
# img = Image.fromarray(np.array(np.random.randint(0,255,(300,300,3)),dtype="uint8").reshape(300,300,3))
# img_byte_arr = io.BytesIO()
# img.save(img_byte_arr, format='PNG')
# # img_byte_arr = img_byte_arr.getvalue()
# print(type(img_byte_arr),type(open("file.jpg","rb")))


import requests
import json
data = [
    {
        "personId": "176cf1d2-15cc-467d-a442-ddcbc86a2cd9",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "1d8ee3b9-dba1-4e1a-bfb7-df3b84803575",
        "persistedFaceIds": [
            "acda8e52-45bc-402f-af52-bb61c9fb1ea4"
        ],
        "name": "deepak"
    },
    {
        "personId": "22a04483-3814-4bff-a5a7-d64854266e39",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "3bdd84dc-095f-4173-924a-6e51c15427db",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "3c1d952d-debf-4cb5-9dbc-43188738e316",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "4a1cb881-3864-4eaf-a05f-c3a177f118de",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "5f00e58d-6e77-408c-8c4e-128288ae9415",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "87a80cbf-3087-475f-b8d6-6d1eb8321e46",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "89164407-bce5-42e6-9158-e59874e71e3e",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "9f078bdc-6ae2-4b02-ae2c-ae434378516d",
        "persistedFaceIds": [],
        "name": "deepak"
    },
    {
        "personId": "bdb1748a-41af-421b-beab-88defa7b109e",
        "persistedFaceIds": [],
        "name": "deepak"
    }
]


ids = [d["personId"] for d in data]
print(ids)
for id_ in ids:
    url = f"https://apifaceverificationproject.cognitiveservices.azure.com/face/v1.0/persongroups/81884a09-940e-4bbc-a581-7ba2ef010e09/persons/{id_}"
    headers = {
        'Ocp-Apim-Subscription-Key': '1a64adf056be45f3b229373bbd4f6bfe',
        'Content-Type': 'application/json'
    }
    # send delete request
    r = requests.delete(url, headers=headers)
    if r.status_code == 200:
        print("deleted")
    else:
        print("error")
        print(r.text)