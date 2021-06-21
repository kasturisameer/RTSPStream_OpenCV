import asyncio
import logging
import signal
import threading

import cv2
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import json
import os
import time
from AzureBlobHelper import AzureBlobHelper
import io
import numpy as np
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = FastAPI()

azureBlobHelper = AzureBlobHelper()
class Stream(BaseModel):
    rtsp: str

@app.get("/delete_stream/{stream_id}")
async def delete_stream(stream_id):
    stream_manager.delete_stream(stream_id)
    logger.info("Delete stream {}".format(stream_id))

    return "ok"


@app.get("/streams/{stream_id}")
async def read_stream(stream_id):
    return {}


is_running = True

@app.post("/streams")
async def create_stream(stream: Stream):
    print("api call")

    rtspurl = stream.rtsp
    # cam = cv2.VideoCapture(rtspurl, cv2.CAP_FFMPEG)
    cam = cv2.VideoCapture(rtspurl, cv2.CAP_FFMPEG)

    # cam.open()
    framescount = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    print(int(cam.get(cv2.CAP_PROP_FRAME_COUNT)))
    cam.set(cv2.CAP_PROP_POS_FRAMES, 0) 

    fps = 10
    isalive = True
    IMG_WIDTH = 960
    IMG_HEIGHT = 540
    cnt = 0
    print("hello")

    if cam.isOpened():
        cam_fps = cam.get(cv2.CAP_PROP_FPS)
        if cam_fps > 0.0 and cam_fps < fps:
            fps = cam_fps
    while isalive:
        print("inside while")
        logger.info(cnt)

        is_ok, img = cam.read()
        print(is_ok)
        # print(img)

        if is_ok:
            width = IMG_WIDTH
            ratio = IMG_WIDTH / img.shape[1]
            height = int(img.shape[0] * ratio + 0.000001)
            if height >= IMG_HEIGHT:
                height = IMG_HEIGHT
                ratio = IMG_HEIGHT / img.shape[0]
                width = int(img.shape[1] * ratio + 0.000001)
            time.sleep(1)
            img = cv2.resize(img, (width, height))
            is_success,im_buf_arr=cv2.imencode(".jpg",img)
            io_buf = io.BytesIO(im_buf_arr)
            cnt += 1

            # azureBlobHelper.upload_file(f'/opencv/images/img_{cnt}.jpg', io_buf)
            # logger.info("reading image")
            logger.info(str(img))

            last_img = img
            last_update = time.time()
            time.sleep(1 / fps)
            print(cnt)

            # print(jpg)
            if (cnt == framescount):
                isalive = False
        else:
            isalive = False
            logger.info("isalive = false")
    print('count is')
    print(cnt)
    return {}


def main():
    uvicorn.run(app, host="0.0.0.0", port=9000)
    # stream = Stream()
    # stream.stream_id = "streamid"
    # stream.rtsp = "rtsp://127.0.0.1:554/media/video.mkv"
    # stream.fps = 10
    # stream.endpoint = "rtsp://127.0.0.1:554/media/video.mkv"
    # create_stream(stream)


if __name__ == "__main__":
    main()


# def handler(signum, frame):
#    global is_running
#    is_running = False
# loop = asyncio.get_event_loop()
# loop.add_signal_handler(signal.SIGINT, handler)
