from setuptools import setup, find_packages
from os import path
import re


here = path.dirname(__file__)


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def read(*names, **kwargs):
    with open(
        path.join(here, *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='bin2coe',

    python_requires='>=3.4',

    version=find_version('src', 'bin2coe', '__init__.py'),

    description='A tool to convert binary files to COE files',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/anishathalye/bin2coe',

    author='Anish Athalye',
    author_email='me@anishathalye.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',

        'Topic :: Utilities',
    ],

    keywords='xilinx coe bram',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'bin2coe=bin2coe.cli:main',
        ],
    },
)
