import os
import unittest
from face_lock.utils import (
    image_encoder,
    servo,
    video_capture
)


class TestUtils(unittest.TestCase):

    def setUp(self):

        RESOLUTION = (480, 320)
        FRAME_RATE = 30
        VIDEO_SIZE = (480, 320)

        self.TEST_IMAGE_DIR = 'face_lock/tests/test_data/test_images'

        self.servo_controller = servo.ServoController(gpio=17)
        self.video_stream = video_capture.VideoCapture(
            resolution=RESOLUTION,
            frame_rate=FRAME_RATE,
            video_size=VIDEO_SIZE
        )
        self.encoder = image_encoder.ImageEncoder(
            image_dir=self.TEST_IMAGE_DIR
        )
        self.images = [
            f for f in os.listdir(self.TEST_IMAGE_DIR) if not f.startswith('.')
        ]


    def test_image_loading(self):
        assert len(self.images) == 4


    def test_image_encoding(self):
        encodings = self.encoder.encode()
        assert bool(encodings)
        assert len(encodings) == len(self.images)


    def test_servo_rotate(self):
        test_pulse_widths = [500, 1000, 1500]
        self.servo_controller.rotate_servo(test_pulse_widths)
        assert self.servo_controller.rotated


    def test_video_capture(self):
        counter = 0
        for frame in self.video_stream.start_video(format='bgr'):
            if counter < 100:
                assert frame.array
                counter += 1
            else:
                break
