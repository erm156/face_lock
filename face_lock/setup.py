from setuptools import setup, find_packages


with open('README.md') as in_file:
    readme = in_file.read()

with open('LICENSE') as in_file:
    license = in_file.read()

setup(
    name='face_lock',
    version='0.1.0',
    description='face-recognition-based servo control on Raspberry Pi',
    long_description=readme,
    author='Eric Miller',
    author_email='ermiller@alumni.cmu.edu',
    url='https://github.com/erm156/face_lock',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
