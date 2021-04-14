# -*- coding: utf-8 -*-

"""
SPDX-FileCopyrightText: 2020 Yinlin Hu <huyinlin@gmail.com>
SPDX-FileCopyrightText: 2021 Manuel Geißer <geisserml@gmail.com>

SPDX-License-Identifier: MIT
"""

from setuptools import setup
from pypdfium import __version__

def readme():
    with open('README.md') as f:
        return f.read()
    
setup(
      name='pypdfium',
      version=__version__,
      description='A simple python wrapper for PDFium',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='Python PDFium',
      url='https://github.com/YinlinHu/pypdfium',
      author='Yinlin Hu',
      author_email='huyinlin@gmail.com',
      maintainer='Manuel Geißer',
      maintainer_email='geisserml@gmail.com',
      license='MIT License',
      packages=['pypdfium'],
      install_requires=[''], #external packages as dependencies
      classifiers=[
      'License :: OSI Approved :: MIT License',
      'Operating System :: POSIX :: Linux',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Microsoft :: Windows',
      'Programming Language :: Python :: 3',
      ],
      include_package_data=True,
      zip_safe=False
)
