import codecs
import os

from setuptools import find_packages, setup

with codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'), mode='r', encoding='utf-8') as readme:
    README = readme.read()

with codecs.open('requirements.txt', mode='r', encoding='utf-8') as file:
    requirements = file.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='readableCodeMatrix',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='This is code readable check Package',
    long_description=README,
    url='https://github.com/kmu-yoonsh/ReadableCodeMatrix',
    author='Hwang Sek-Jin',
    author_email='dollking@kookmin.ac.kr',
    classifiers=[
        'Intended Audience :: Developers, Educator',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
