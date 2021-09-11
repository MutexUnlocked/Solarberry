import io
import picamera
import base64
import numpy as np
import cv2
import logging
import socketserver
from threading import Condition
from http import server

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                # Setup image frame for CV2
                jpg_original = base64.b64decode(self.frame)
                jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
                img = cv2.imdecode(jpg_as_np, flags=1)
                
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                h,s,v = cv2.split(img_hsv)
                mean_pixel = np.mean(v)
                print(mean_pixel)

                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

with picamera.PiCamera(resolution='1920x1080', framerate=30) as camera:
    output = StreamingOutput()
    camera.brightness = 55
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='jpeg')
    #try:
    #    address = ('10.95.156.184', 7070)
    #    server = StreamingServer(address, StreamingHandler)
    #    server.serve_forever()
    #finally:
    #    camera.stop_recording()
