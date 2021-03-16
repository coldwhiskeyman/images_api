import time

from database import Image


def process_image(img_id):
    time.sleep(5)
    Image.process_complete(img_id)
