import glob
import subprocess
from setuptools import setup, find_packages, Extension


def build_libs():
    retcode = subprocess.call(['cmake', '.'])

    if retcode != 0:
        exit(retcode)

    retcode = subprocess.call(['make'])

    if retcode != 0:
        exit(retcode)
    

build_libs()


setup(
    name='jetbot',
    version='0.4.3',
    description='An open-source robot based on NVIDIA Jetson Nano',
    packages=find_packages(),
    install_requires=[
        'Adafruit_MotorHat',
        'Adafruit-SSD1306',
    ],
    package_data={'jetbot': ['ssd_tensorrt/*.so']},
)
