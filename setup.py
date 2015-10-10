import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-knob',
    version='1.0',
    packages=['knob'],
    include_package_data=True,
    license='GNU GENERAL PUBLIC LICENSE',  
    description='A Django reusable application that performs remote configurations on multiple devices, distributing the operations using python multiprocessing library.',
    long_description=README,
    author='Mohamed Daif',
    author_email='muhammad.daif@gmail.com',
    install_requires = ['exscript==2.1.479'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
