# -*- coding: utf-8 -*-

import sys
from os import system
from pathlib import Path
from shutil import rmtree
from setuptools import setup, Command


VERSION = '0.0.1'

HERE = Path(__file__).parent


class UploadCommand(Command):
    """Support for setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(HERE / 'dist')
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        system(f'{sys.executable} setup.py sdist bdist_wheel')

        self.status('Uploading the package to PyPI via Twine...')
        system('twine upload dist/*')

        self.status('Pushing git tags...')
        system(f"git tag v{VERSION}")
        system('git push --tags')

        sys.exit()


setup(
    name='HCSR04_python_lib',
    version=VERSION,
    description='Library for HC-SR04 ultrasonic distance sensor used with Raspberry Pi.',
    long_description_content_type="text/markdown",
    long_description=open(HERE / "README.md", "r", encoding="utf-8").read(),
    author='Jakub Przepiórka',
    author_email='jakub.przepiorka.contact.me@gmail.com',
    python_requires='>=3.9',
    url='https://github.com/JakubPrz/HCSR04_python_lib',
    download_url='https://github.com/JakubPrz/HCSR04_python_lib/archive/v0.0.1.tar.gz',
    install_requires=['RPi.GPIO'],  # == 0.7.0
    packages=['HCSR04_python_lib'],
    license='MIT',
    platforms=['Linux'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
