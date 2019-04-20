from setuptools import setup

setup(
    name='GenshiBASIC-Interpreter',
    url='https://github.com/barrettotte/GenshiBASIC-Interpreter',
    author='Barrett Otte',
    author_email='barrettotte@gmail.com',
    packages=['GenshiBas'],
    install_requires=[],
    version='0.1',
    license='MIT',
    description='An interpreter for Genshi BASIC; A simpler implementation of BASIC based off of Commodore 64 BASICv2',
    long_description=open('README.md').read(),
)