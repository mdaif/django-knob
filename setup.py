import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-knob',
    url="https://github.com/mdaif/django-knob",
    version='1.1',
    packages=['knob'],
    include_package_data=True,
    license='OSI Approved',  # example license
    description='A Django reusable application that performs remote configurations on multiple devices, distributing the operations using Celery.',
    long_description=README,
    author='Mohamed Daif',
    author_email='muhammad.daif@gmail.com',
    install_requires = ['exscript==2.1.479', 'Django>=1.8.3', 'celery==3.1.18',
    'django-celery==3.1.16'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
