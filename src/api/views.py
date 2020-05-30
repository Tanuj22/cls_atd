import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
import os
from numpy import asarray

from django.conf import settings
from PIL import Image as PImage
import cv2
from mtcnn import MTCNN
import json


def upload_image(request):
    img = request.FILES['image']
    img_extension = os.path.splitext(img.name)[-1]
    return default_storage.save(settings.MEDIA_URL + str(uuid.uuid4()) + img_extension, img)


def detect_faces(image_path):
    image = PImage.open(default_storage.open(image_path))
    image = image.convert('RGB')
    pixels = asarray(image)

    detector = MTCNN()
    result = detector.detect_faces(pixels)
    num_of_faces = len(result)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, 'LightCNN')
    path = os.path.join(path, 'data')
    os.chdir(path)
    j = 0
    for i in range(0, num_of_faces):
        bounding_box = result[i]['box']
        keypoints = result[i]['keypoints']
        tempim = pixels[bounding_box[1]:(bounding_box[1] + bounding_box[3]),
                 bounding_box[0]:(bounding_box[0] + bounding_box[2])]
        cv2.imwrite("face_{}.jpg".format(j + 1), cv2.cvtColor(tempim, cv2.COLOR_RGB2BGR))
        j = j + 1


class Image(APIView):

    def post(self, request, *args, **kwargs):
        upload = upload_image(request=request)
        detect_faces(upload)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'LightCNN')
        get_list = os.path.join(path, 'get_list.py')
        extract_feat = os.path.join(path, 'extract_features.py')
        cosine = os.path.join(path, 'cossim.py')
        os.chdir(path)
        os.system(f'python {get_list}')
        os.system(f'python {extract_feat}')
        os.system(f'python {cosine}')
        attendance = os.path.join(path, 'attendance.json')
        f = open(attendance, )
        data = json.load(f)
        f.close()
        return Response(data, status=status.HTTP_200_OK)
