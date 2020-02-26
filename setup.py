from setuptools import setup
from setuptools import find_packages

long_description = '''
Python module to Convert a  PDF file to a JSON format

The goal is to be able to quickly extract all the available information in the document to a python dictionay. The dictionay can then be stored in a database or a csv file (for a later Machine Learning processing).

The extracted information can be :
* Document metadata : title, format, versino, creation date, author
* Page images
* Page texts (in Unicode) and attirbutes (fonts etc)

This tool uses the excellent [poppler](https://poppler.freedesktop.org/) library. It is initially intended for multilingual PDF document processing.
'''

setup(name='pdf_to_json',
      version='0.1',
      description='Convert a  PDF file to a JSON format',
      long_description=long_description,
      author='Antoine CARME',
      author_email='Antoine.Carme@laposte.net',
      url='https://github.com/antoinecarme/pdf_to_json',
      license='BSD',
      install_requires=['PyGObject'],
      extras_require={
      },
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=find_packages())
