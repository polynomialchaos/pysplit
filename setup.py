from setuptools import setup, find_packages

setup(
    name='pysplit',
    version='1.0',
    description='A simple python package for money pool split development.',
    author='Florian',
    author_email='polynomialchaos@gmail.com',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            'pySplit=pysplit.bin.pySplit:main',
        ]
    }
)
