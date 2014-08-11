import re
import importlib
from django.utils import six
from django.utils.module_loading import import_string
from django.conf import settings, BaseSettings


def underscore_capitalized(str):
    return re.sub('(((?<=[a-z])[A-Z1-9])|([A-Z1-9](?![A-Z1-9]|$)))', '_\\1', str).strip('_').upper()


class AppSettingsHolder(BaseSettings):

    def __init__(self, app_settings_module, user_settings_key, import_strings=None):

        self.SETTINGS_MODULE = app_settings_module

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError as e:
            raise ImportError("Could not import app settings '{}' (Is it on sys.path? Is there an import error in the settings file?): {}".format(self.SETTINGS_MODULE, e))

        self._user_settings_key = user_settings_key
        self._import_strings = import_strings or []
        self._app_settings = {setting: getattr(mod, setting) for setting in dir(mod) if setting.isupper()}
        self._user_settings = getattr(settings, user_settings_key, None)

    def _perform_import(self, value, setting_name):
        try:
            if isinstance(value, six.string_types):
                return import_string(value)
            elif isinstance(value, (list, tuple)):
                return [import_string(item) for item in value]
        except ImportError as e:
            raise ImportError("Could not import '{}' for {} app setting '{}'. {}: {}".format(value, self._user_settings_key, setting_name, e.__class__.__name__, e))

    def __getattr__(self, attr):
        if attr not in self._app_settings.keys():
            raise AttributeError("Invalid {} setting: '{}'".format(self._user_settings_key, attr))

        # Check if present in user settings and return app default otherwise
        try:
            value = self._user_settings[attr]
        except:
            value = self._app_settings[attr]

        # Coerce import strings into classes
        if value and attr in self._import_strings:
            value = self._perform_import(value, attr)

        # Cache the result
        setattr(self, attr, value)
        return value


class AppSettingsMeta(type):

    def __init__(cls, name, bases, dict):
        cls.settings_module = cls.settings_module if hasattr(cls, 'settings_module') else None
        cls.settings_key = cls.settings_key.upper() if hasattr(cls, 'settings_key') else underscore_capitalized(name)
        cls.settings_imports = cls.settings_imports if hasattr(cls, 'settings_imports') else None

        if cls.settings_module:
            cls.settings = AppSettingsHolder(cls.settings_module, cls.settings_key, cls.settings_imports)
        else:
            cls.settings = None

        super(AppSettingsMeta, cls).__init__(name, bases, dict)


class AppSettings(six.with_metaclass(AppSettingsMeta)):

    def __getattr__(self, attr):
        return getattr(self.settings, attr)
