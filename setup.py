import sys
import os
import re
import codecs
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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


VERSION = read("VERSION").strip()

REPO_URL = "https://github.com/jthi3rry/django-pods"

PYPI_README_NOTE = """\
.. note::

   For the latest source, discussions, bug reports, etc., please visit the `GitHub repository <{}>`_
""".format(REPO_URL)

LONG_DESCRIPTION = "\n\n".join([PYPI_README_NOTE, read("README.rst")])


setup(
    name='django-pods',
    version=VERSION,
    author='OohlaLabs Limited',
    author_email='packages@oohlalabs.co.nz',
    maintainer="Thierry Jossermoz",
    maintainer_email="thierry.jossermoz@oohlalabs.com",
    url=REPO_URL,
    packages=find_packages(exclude=("tests*",)),
    install_requires=['Django', ],
    tests_require=['tox', 'nose', ],
    cmdclass={'test': Tox},
    license='MIT',
    description='App Settings for Django',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Framework :: Django",
    ]
)
