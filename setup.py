from setuptools import setup

setup(
    name='pysplit',
    version='1.0',
    description='A simple python package for money pool split development.',
    author='Florian',
    author_email='polynomialchaos@gmail.com',
    packages=['pysplit'],
    entry_points={
        "console_scripts": [
            'pySplit=bin.pySplit:main',
        ]
    }
)