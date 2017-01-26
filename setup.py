#!/usr/bin/env python

from distutils.core import setup

setup(
    name='qgisrv',
    version='0.1.0',
    description='QGIS Plugin Server',
    author='Thomas Kager',
    author_email='tablet-mode@monochromatic.cc',
    license='MIT',
    keywords=['qgis', 'server'],
    url='http://www.github.com/~tablet-mode/qgisrv',
    packages=['qgisrv'],
    long_description=open('README').read(),
    install_requires=[
        'tornado',
        'lxml',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
