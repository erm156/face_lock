import os
import re
from face_recognition import load_image_file, face_encodings


class ImageEncoder:


    def __init__(self, image_dir='face_lock/data/src_images'):
        if not len([f for f in os.listdir(image_dir) if not f.startswith('.')]) == 0:
            self.image_files = sorted(os.listdir(image_dir))

            if all([len(re.split('[_.]', image_file)) == 3 for image_file in self.image_files]):
                self.names = sorted([
                    ' '.join(re.split('[_.]', name)[:2].title()) for name in self.image_files
                ])
            else:
                raise NameError(
                    f'Names of files in {image_dir} are not properly formatted (fname_lname.ext)'
                )
        else:
            raise FileNotFoundError(f'No images available for encoding ({image_dir} is empty)')

    def encode(self):
        faces = [
            load_image_file(image_file) 
            for image_file in self.image_files 
            if not image_file.startswith('.')
        ]

        self.encodings = [
            face_encodings(face)[0] for face in faces
        ]

        return dict(zip(self.names, self.encodings))
