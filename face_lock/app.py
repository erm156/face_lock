import logging
import time
from datetime import datetime as dt
import face_recognition
import image_encoder
import video_capture
import servo


LOG_FILENAME = 'face_log.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,
    format='%(asctime)s %(name)-4s %(levelname)-8s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S'
)

logging.getLogger(name='FACE_LOG')
logging.info('Loading known face encodings...')

image_encoder = ImageEncoder()
known_encodings = image_encoder.encode()

logging.info('Initializing video...')

video = VideoCapture(
    resolution=(480, 320),
    frame_rate=30,
    video_size=(480, 320)
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

                    logging.info(f'{name} @ {str(dt.now())}')

                    if len(face_names) > 0:
                        logging.info(
                            f'{str(len(face_names))} known face(s) detected: {face_names}'
                        )
                    
                    PULSE_WIDTHS = [500, 1500, 500]
                    servo_control.rotate_servo(PULSE_WIDTHS)
                    continue       
                else:
                    face_names.append("Unknown")
                    unknowns = [name for name in face_names if name == 'Unknown']
                    logging.info(f'{str(len(unknowns))} UNKNOWN face(s) detected')

    video.flush_video(stream_size=0)