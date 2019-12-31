from picamera import PiCamera
from picamera.array import PiRGBArray


class VideoCapture:


    def __init__(self, resolution, frame_rate, video_size):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = frame_rate
        
        self.raw_capture = PiRGBArray(self.camera, video_size)
        self.process_frame = True

    def start_video(self, format):
        self.video = self.camera.capture_continuous(
            self.raw_capture,
            format=format,
            use_video_port=True
        )

        return self.video

    def flush_video(self, stream_size):
        self.process_frame = not self.process_frame
        self.raw_capture.truncate(stream_size)
