import re
import importlib
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.conf import settings
try:
    from django.utils.module_loading import import_string
except ImportError:  # pragma: no cover
    from django.utils.module_loading import import_by_path as import_string


def underscore_capitalized(s):
    return re.sub('(((?<=[a-z])[A-Z1-9])|([A-Z1-9](?![A-Z1-9]|$)))', '_\\1', s).strip('_').upper()


# copied from django<1.11
class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    def __setattr__(self, name, value):
        if name in ("MEDIA_URL", "STATIC_URL") and value and not value.endswith('/'):
            raise ImproperlyConfigured("If set, %s must end with a slash" % name)
        object.__setattr__(self, name, value)


class AppSettingsHolder(BaseSettings):

    def __init__(self, app_settings_module, user_settings_key, import_strings=None):

        self.SETTINGS_MODULE = app_settings_module

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError as e:
            raise ImportError("Could not import app settings '{}' "
                              "(Is it on sys.path? Is there an import error in the settings file?): {}".format(self.SETTINGS_MODULE, e))
        self._user_settings_key = user_settings_key
        self._import_strings = import_strings or []
        self._app_settings = {setting: getattr(mod, setting) for setting in dir(mod) if setting.isupper()}
        self._user_settings = getattr(settings, user_settings_key, {})

    def _perform_import(self, value, setting_name):
        try:
            if isinstance(value, six.string_types):
                return import_string(value)
            elif isinstance(value, (list, tuple)):
                return [import_string(item) for item in value]
        except (ImportError, ImproperlyConfigured) as e:
            raise ImportError("Could not import module '{}' "
                              "(Have you checked the setting '{}' for app '{}'?): {}".format(value, self._user_settings_key, setting_name, e))

    def _get_user_setting(self, name):
        try:
            return self._user_settings[name]
        except (KeyError, TypeError):
            try:
                return getattr(settings, '_'.join([self._user_settings_key, name]))
            except AttributeError:
                return self._app_settings[name]

    def __getattr__(self, attr):
        if attr not in self._app_settings.keys():
            raise AttributeError("Invalid {} setting: '{}'".format(self._user_settings_key, attr))

        value = self._get_user_setting(attr)

        # Coerce import strings into classes
        if value and attr in self._import_strings:
            value = self._perform_import(value, attr)

        # Cache the result
        setattr(self, attr, value)
        return value


class AppSettingsMeta(type):

    def __init__(cls, name, bases, data):
        cls.settings_module = data.pop('settings_module', None)
        cls.settings_key = data.pop('settings_key', underscore_capitalized(name)).upper()
        cls.settings_imports = data.pop('settings_imports', None)

        if cls.settings_module:
            cls.settings = AppSettingsHolder(cls.settings_module, cls.settings_key, cls.settings_imports)
        else:
            cls.settings = None

        super(AppSettingsMeta, cls).__init__(name, bases, data)

    def __getattr__(cls, attr):
        return getattr(cls.settings, attr)


class AppSettings(six.with_metaclass(AppSettingsMeta)):

    def __getattr__(self, attr):
        return getattr(self.settings, attr)
