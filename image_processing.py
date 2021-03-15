import time

FILES_IN_WORK = {}


def process_image(filename):
    FILES_IN_WORK[filename] = False
    time.sleep(5)
    FILES_IN_WORK[filename] = True
