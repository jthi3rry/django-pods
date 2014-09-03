===========
Django Pods
===========

.. image:: https://pypip.in/version/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://pypip.in/format/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://travis-ci.org/OohlaLabs/django-pods.svg?branch=master
    :target: https://travis-ci.org/OohlaLabs/django-pods

.. image:: https://coveralls.io/repos/OohlaLabs/django-pods/badge.png?branch=master
    :target: https://coveralls.io/r/OohlaLabs/django-pods

.. image:: https://pypip.in/py_versions/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://pypip.in/license/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

Django Pods is a minimalist package that lets you configure app specific settings that can be overridden in project settings.

This package is largely inspired by `Django Rest Framework <http://www.django-rest-framework.org/>`_ and `Django AllAuth <http://www.intenct.nl/projects/django-allauth/>`_ and adapted to work with `Django 1.7 Applications <https://docs.djangoproject.com/en/dev/ref/applications/>`_, but also with any classes extending ``pods.apps.AppSettings``.


Installation
------------
::

    pip install django-pods


Django 1.7 Usage
----------------

In ``rock_n_roll/apps.py``::


    from django.apps import AppConfig
    from pods.apps import AppSettings


    class RockNRollConfig(AppSettings, AppConfig):
        name = 'rock_n_roll'
        verbose_name = "Rock ’n’ roll"

        # Path to app settings module
        settings_module = "rock_n_roll.app_settings"

        # Optional
        settings_imports = ("CLASS_TO_IMPORT",)

        # Optional
        # defaults to the capitalized class name, e.g. ROCK_N_ROLL_CONFIG
        settings_key = "ROCK_N_ROLL"


In ``rock_n_roll/app_settings.py``::


    QUESTION = "What is your favourite band?"
    ANSWER = "The Rolling Stones"
    CLASS_TO_IMPORT = "path.to.ClassToImport"


In ``project/settings.py``::


    ROCK_N_ROLL = {
        "ANSWER": "The Beatles",
    }


Anywhere else in your project::


    from django.apps import apps

    app = apps.get_app_config('rock_n_roll')

    app.settings.QUESTION
    # What is your favourite band?

    app.settings.ANSWER
    # The Beatles

    app.settings.CLASS_TO_IMPORT
    # <class 'path.to.ClassToImport'>


``AppSettings`` also implements ``__getattr__`` to proxy to settings attributes::


    app.ANSWER
    # The Beatles


Django < 1.7 Usage
------------------

There isn't a logical place to create a class representing an app in Django prior to 1.7, but any class can extend ``AppSettings``::

    from pods.apps import AppSettings


    class AnyClass(AppSettings):
        settings_module = "path.to.settings"


    AnyClass.settings

    # or

    a = AnyClass()
    a.settings


Running Tests
-------------
::

    tox


Contributions
-------------

All contributions and comments are welcome.

Change Log
----------

v0.3
~~~~
* Unit tests now use Django 1.7 final and support Django 1.6 and 1.5
* Fix PyPI classifiers for supported python versions

v0.2
~~~~
* Fix compatibility with Django 1.6

v0.1
~~~~
* Initial
