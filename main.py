import time
import cv2
import numpy as np
from utils import *

def clip_generator(cam):
    image_queue = []
    while True:
        ret, frame = cam.read()
        if not ret:
            return
        image_queue.append(frame)
        if len(image_queue) < NB_IMAGES_PER_CLIP:
            image_queue.append(frame)
        elif len(image_queue) > NB_IMAGES_PER_CLIP:
            image_queue = image_queue[1:]
        if len(image_queue) == NB_IMAGES_PER_CLIP:
            yield np.array(image_queue)

def write_clip(clip):
    fps = 1/INTERVAL
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output/output.avi', fourcc, fps, (WIDTH, HEIGHT))
    for frame in clip:
        out.write(frame)
    out.release()

cam = cv2.VideoCapture(0)
clips = clip_generator(cam)
while True:
    clip = next(clips)
    print(clip.shape)
    write_clip(clip)
    time.sleep(INTERVAL)