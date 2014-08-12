import sys
import os
import re
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-pods',
    version=find_version('pods', '__init__.py'),
    author='OohlaLabs Limited',
    author_email='packages@oohlalabs.co.nz',
    url='https://github.com/OohlaLabs/django-pods',
    packages=find_packages(),
    install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt')],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    license='Copyright 2014 OohlaLabs Limited',
    description='App Settings for Django 1.7',
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Framework :: Django",
    ]
)