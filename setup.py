
from setuptools import setup
from pypdfium import __version__

setup(
      name='pypdfium',
      version=__version__,
      description='simple python wrapping of PDFium',
      keywords='PDFium',
      url='',
      author='Yinlin Hu',
      author_email='huyinlin@gmail.com',
      license='MIT',
      packages=['pypdfium'],
      install_requires=[''], #external packages as dependencies
      classifiers=[
      'License :: OSI Approved :: MIT',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3',
      ],
      include_package_data=True,
      zip_safe=False
)
