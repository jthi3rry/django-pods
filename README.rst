===========
Django Pods
===========

.. image:: https://pypip.in/version/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://pypip.in/format/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://travis-ci.org/jthi3rry/django-pods.svg?branch=master
    :target: https://travis-ci.org/jthi3rry/django-pods

.. image:: https://coveralls.io/repos/jthi3rry/django-pods/badge.png?branch=master
    :target: https://coveralls.io/r/jthi3rry/django-pods

.. image:: https://landscape.io/github/jthi3rry/django-pods/master/landscape.png
    :target: https://landscape.io/github/jthi3rry/django-pods/master

.. image:: https://pypip.in/py_versions/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

.. image:: https://pypip.in/license/django-pods/badge.svg
    :target: https://pypi.python.org/pypi/django-pods/

Django Pods is a minimalist package that lets you configure default settings for your `reusable apps <https://docs.djangoproject.com/en/dev/intro/reusable-apps/>`_, and allows developers using your apps to override these defaults in their own project settings.

This package is largely inspired by `Django Rest Framework <http://www.django-rest-framework.org/>`_ and `Django AllAuth <http://www.intenct.nl/projects/django-allauth/>`_ and adapted to work with `Django Applications <https://docs.djangoproject.com/en/dev/ref/applications/>`_, but also with any classes extending ``pods.apps.AppSettings``.


Preview
-------

Django Pods allows developers to customise app settings in two ways:


1. Dictionary style (as per `Django Rest Framework <http://www.django-rest-framework.org/>`_)::


    YOUR_APP = {
        "SETTING": "VALUE"
    }


2. Prefix style::


    YOUR_APP_SETTING = "VALUE"


Installation
------------
::

    pip install django-pods


Usage in Reusable Apps
----------------------

1. Add ``django-pods`` to the ``install_requires`` of your ``setup.py``::


    setup(
        name="rock_n_roll",
        install_requires=["django-pods", ...],
        ...
    )


2. Add the ``AppSettings`` mixin to your AppConfig implementation in ``rock_n_roll/apps.py``::


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


3. Declare your default app settings in ``rock_n_roll/app_settings.py``::


    QUESTION = "What is your favourite band?"
    ANSWER = "The Rolling Stones"
    CLASS_TO_IMPORT = "path.to.ClassToImport"


4. Access your settings anywhere in your package::


    from django.apps import apps

    app = apps.get_app_config('rock_n_roll')

    app.QUESTION
    # What is your favourite band?

    app.ANSWER
    # The Beatles

    app.CLASS_TO_IMPORT
    # <class 'path.to.ClassToImport'>


Settings can also be accessed directly via the class::


    from rock_n_roll.apps import RockNRollConfig


    RockNRollConfig.QUESTION
    RockNRollConfig.ANSWER
    RockNRollConfig.CLASS_TO_IMPORT


.. note:: **AppSettings ``settings`` Property**

    ``AppSettings`` implements ``__getattr__`` to proxy to the ``settings`` attributes of the class::


        app.QUESTION == app.settings.QUESTION

        # or

        RockNRollConfig.QUESTION == RockNRollConfig.settings.QUESTION


.. note:: **Usage with Django < 1.7**

    Prior to Django 1.7, there wasn't a logical place to create a class representing an app. However, any class can extend ``AppSettings``. For example, in ``models.py``::

        from pods.apps import AppSettings


        class AnyClass(AppSettings):
            settings_module = "rock_n_roll.app_settings"


    Import your app class directly::

        from .models import AnyClass

        AnyClass.QUESTION



Usage in Projects
-----------------


1. Install the app that uses Django Pods::

 
    pip install rock_n_roll


2. Add the app to the ``INSTALLED_APPS`` of your ``project/settings.py``::


    INSTALLED_APPS = (
        ...
        "rock_n_roll",
        ...
    )


3. Override the app's settings as needed::


    # Dictionary style
    ROCK_N_ROLL = {
        "ANSWER": "The Beatles",
    }


    # Prefix style
    ROCK_N_ROLL_ANSWER = "The Beatles"


Running Tests
-------------
::

    tox


Contributions
-------------

All contributions and comments are welcome.

Change Log
----------

v1.1.2
~~~~~~
* Django 1.8 support

v1.1.1
~~~~~~
* Switch to Semantic Versioning
* Fix issue with parse_requirements for newer versions of pip (>=6.0.0)
* Fix typo in AppSettingsMeta

v1.1
~~~~
* Exclude tests and docs from the build

v1.0
~~~~
* Add support for prefix style overrides
* Documentation changes

v0.4
~~~~
* Fix bug with default settings_key not set correctly if none given

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
