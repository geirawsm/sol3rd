from setuptools import setup, find_packages
from os import path
from io import open
from sol3rd.__version__ import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='sol3rd',
    version=version,
    description='Install 3rd party apps in Solus or upgrade them',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-v3.0',
    author='armandg',
    author_email='armandg@gmail.com',
    entry_points={
        'console_scripts': [
            'sol3rd = sol3rd.sol3rd:main'
        ]
    },
    packages=find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'html5lib',
        'colorama'
    ],
    package_data={
        'sol3rd': [
            '__version__.py'
        ]
    }
)
