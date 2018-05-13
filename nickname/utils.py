import os

from django.conf import settings
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import nets.resnet_v1 as resnet
from PIL import Image as Pil_image
import random

from .models import Category, Nickname


def ing_models(extracted_img_list):
    # VARIABLES
    # CKPT_PATH = "cosmetic-300/cosmetic-300"
    CKPT_PATH = os.path.join(settings.BASE_DIR + 'cosmetic-300/cosmetic-300')
    MEAN_PIXEL = [123.68, 116.78, 103.94]
    NCLASS = 12

    inputs = tf.placeholder(tf.float32, [None, 224, 224, 3])
    is_training = tf.placeholder(tf.bool)

    # MODEL PREPARATION
    with slim.arg_scope(resnet.resnet_arg_scope()):
        logit, model = resnet.resnet_v1_50(inputs, num_classes=NCLASS, is_training=is_training)

    init_fn = slim.assign_from_checkpoint_fn(CKPT_PATH,
                                             slim.get_variables_to_restore(),
                                             ignore_missing_vars=True)

    # CREATE SESSION
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    init_fn(sess)

    predict_list = []
    if extracted_img_list:
        for extracted_img in extracted_img_list:
            x = Pil_image.open(extracted_img.image.path)
            x = x.convert('RGB')
            x = x.resize((224, 224))
            x = np.array(x)
            x = x.astype(np.float32) - MEAN_PIXEL
            predict_images = []
            predict_images.append(x)
            predict_images = np.array(predict_images)
            predict = sess.run(model["predictions"], feed_dict={inputs: predict_images, is_training: False})
            predict = np.argmax(predict, 1)
            predict_list.append(predict)

    category_list = []
    if predict_list:
        for predict in predict_list:
            category = Category.objects.get(id=(int(predict)))
            category_list.append(category)

    nickname_id_list = []
    if category_list:
        for category in category_list:
            nickname_queryset = Nickname.objects.filter(category=category)
            if nickname_queryset:
                nickname_id = nickname_queryset[random.randrange(0, len(nickname_queryset))].id
                nickname_id_list.append(nickname_id)

    nickname_list = Nickname.objects.filter(id__in=nickname_id_list)

    return nickname_list
