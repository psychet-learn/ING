import os

from django.conf import settings
from object_extractor import Extractor, FRONTALFACE_ALT2
import cv2

from .models import Image, ExtractedImage
from nickname.utils import ing_models


def extracted_image_path(image_path, count):
    file = image_path.split('/')[-1]
    file_name = file.split('.')[0] + '_extracted_' + str(count) + '.' + file.split('.')[1]

    return os.path.join('faces/extracted', file_name)


def extract(image_path,
            size=(224, 224),
            scale_factor=1.1,
            min_neighbors=5,
            min_size=(50, 50),
            cascade_file=FRONTALFACE_ALT2):
    """ Extract the objects from image and return number of objects detected
    image_path -- The path of the image.
    size -- Size of face images (default None - no rescale at all)
    image -- The image (numpy matrix) read by readImage function.
    min_size -- Minimum possible object size. Objects smaller than that are ignored (default (50,50)).
    scale_factor -- Specifying how much the image size is reduced at each image scale (default 1.1).
    min_neighbors -- Specifying how many neighbors each candidate rectangle should have to retain it (default 5).
    cascade_file  -- The path of cascade xml file use for detection (default current value)
    output_directory -- Directory where to save output (default None - same as input image)
    output_prefix -- Prefix of output (default None - the name of input image)
    startCout -- Specifying the starting of the number put into output names (default 0)
    """

    image = cv2.imread(image_path)
    objects = detect(image,
                     scale_factor=scale_factor,
                     min_neighbors=min_neighbors,
                     min_size=min_size,
                     cascade_file=cascade_file)

    count = 0
    extracted_img_path_list = []
    for (x, y, w, h) in objects:
        count += 1
        obj = image[y:y + h, x:x + w]
        if size:
            obj = cv2.resize(obj, size)
        cv2.imwrite(os.path.join(settings.MEDIA_ROOT, extracted_image_path(image_path, count)), obj)
        extracted_img_path = extracted_image_path(image_path, count)
        extracted_img_path_list.append(extracted_img_path)

    return extracted_img_path_list


def detect(image,
           min_size=(50, 50),
           scale_factor=1.1,
           min_neighbors=5,
           cascade_file=FRONTALFACE_ALT2):
    """ Return list of objects detected.
    image -- The image (numpy matrix) read by readImage function.
    min_size -- Minimum possible object size. Objects smaller than that are ignored (default (50,50)).
    scale_factor -- Specifying how much the image size is reduced at each image scale (default 1.1).
    min_neighbors -- Specifying how many neighbors each candidate rectangle should have to retain it (default 5).
    cascade_file  -- The path of cascade xml file use for detection (default current value)
    """

    classifier = cv2.CascadeClassifier(cascade_file)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return classifier.detectMultiScale(gray_image,
                                       scaleFactor=scale_factor,
                                       minNeighbors=min_neighbors,
                                       minSize=min_size)


def handle_image_file(image):
    raw_img = Image.create_image(image_file=image)
    extracted_img_path_list = extract(raw_img.image.path)

    extracted_img_id_list = []
    if extracted_img_path_list:
        for extracted_img_path in extracted_img_path_list:
            extracted_img = ExtractedImage()
            extracted_img.image.name = extracted_img_path
            extracted_img.origin_image = raw_img
            extracted_img.save()
            extracted_img_id_list.append(extracted_img.id)

    extracted_img_list = ExtractedImage.objects.filter(id__in=extracted_img_id_list)
    nickname_list = ing_models(extracted_img_list)

    return extracted_img_list, nickname_list

