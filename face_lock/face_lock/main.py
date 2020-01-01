import logging
import time
from datetime import datetime as dt
import face_recognition
from face_lock.utils import (
    image_encoder.ImageEncoder,
    servo.ServoController,
    video_capture.VideoCapture
)


LOG_FILENAME = 'face_log.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='%(asctime)s %(name)-4s %(levelname)-8s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S'
)

logging.getLogger(name='FACE_LOG')
logging.info('Loading known face encodings...')

image_encoder = ImageEncoder()
known_encodings = image_encoder.encode()

logging.info('Initializing video...')

RESOLUTION = (480, 320)
FRAME_RATE = 30
VIDEO_SIZE = (480, 320)

video = VideoCapture(
    resolution=RESOLUTION,
    frame_rate=FRAME_RATE,
    video_size=VIDEO_SIZE
)

servo_control = ServoController(gpio=17)

for frame in video.start_video(format='bgr'):
    if video.process_frame:
        image = frame.array

        face_names = []
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image,
                                                         face_locations)

        if face_locations:
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    list(known_encodings.values()),
                    face_encoding
                )

                if True in matches:
                    first_match = matches.index(True)
                    name = sorted(known_encodings.keys())[first_match]
                    face_names.append(name)

                    logging.info(f'****{name}****')
                    
                    PULSE_WIDTHS = [500, 1500, 500]
                    servo_control.rotate_servo(PULSE_WIDTHS)
                    continue       
                else:
                    face_names.append('Unknown')
                    unknowns = [name for name in face_names if name == 'Unknown']
                    logging.info(f'{str(len(unknowns))} UNKNOWN face(s) detected')

    video.flush_video(stream_size=0)
