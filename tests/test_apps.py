import unittest

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from pods.apps import AppSettings, AppSettingsHolder, underscore_capitalized

settings.configure(
    INSTALLED_APPS=[
        'tests.mocks'
    ],
    MOCK={
        "DICT_STYLE_OVERRIDE": True
    },
    MOCK_PREFIX_STYLE_OVERRIDE=True
)


class TestAppSettings(unittest.TestCase):

    def setUp(self):
        from tests.mocks.apps import MockAppConfig
        self.app = MockAppConfig()

    def test_has_settings(self):
        self.assertTrue(hasattr(self.app, 'settings'))
        self.assertTrue(hasattr(self.app.__class__, 'settings'))
        self.assertIsInstance(self.app.settings, AppSettingsHolder)

    def test_settings_defaults(self):
        from tests.mocks import app_test_settings
        self.assertEqual(self.app.settings.DEFAULT, app_test_settings.DEFAULT)

    def test_settings_override(self):
        from tests.mocks import app_test_settings
        self.assertNotEqual(self.app.settings.DICT_STYLE_OVERRIDE, app_test_settings.DICT_STYLE_OVERRIDE)
        self.assertNotEqual(self.app.settings.PREFIX_STYLE_OVERRIDE, app_test_settings.PREFIX_STYLE_OVERRIDE)

    def test_imports(self):
        from tests.mocks import app_test_imports
        self.assertEqual(self.app.settings.APP_MODULE, app_test_imports.TestClass)

    def test_multiple_imports(self):
        from tests.mocks import app_test_imports
        self.assertListEqual(self.app.settings.MULTIPLE_APP_MODULES, [app_test_imports.TestClass, app_test_imports.OtherTestClass])

    def test_attribute_error(self):
        with self.assertRaises(AttributeError):
            module = self.app.settings.DOES_NOT_EXIST

    def test_import_error(self):
        with self.assertRaises(ImportError):
            module = self.app.settings.NON_EXISTENT_APP_MODULE

    def test_settings_import_error(self):
        with self.assertRaises(ImportError):
            AppSettingsHolder("doesnotexist", "KEY")

    def test_default_settings_key_capitalizer(self):
        self.assertEqual(underscore_capitalized("MockAppConfig"), "MOCK_APP_CONFIG")
        self.assertEqual(underscore_capitalized("MockWithNumber1"), "MOCK_WITH_NUMBER_1")
        self.assertEqual(underscore_capitalized("RockNRollConfig"), "ROCK_N_ROLL_CONFIG")

    def test_settings_proxy(self):
        from tests.mocks.apps import MockAppConfig
        self.assertTrue(hasattr(MockAppConfig, 'DEFAULT'))
        self.assertFalse(hasattr(MockAppConfig, 'DOES_NOT_EXIST'))
        self.assertTrue(hasattr(self.app, 'DEFAULT'))
        self.assertFalse(hasattr(self.app, 'DOES_NOT_EXIST'))

    def test_default_settings_key(self):
        class SettingsKeyClass(AppSettings):
            settings_module = 'tests.mocks.app_test_settings'

        app = SettingsKeyClass()
        self.assertEqual(app.settings_key, 'SETTINGS_KEY_CLASS')

    def test_setattr_legacy(self):
        # Not sure if we actually want this functionality, but for coverage of legacy Django behaviour
        with self.assertRaises(ImproperlyConfigured):
            self.app.settings.MEDIA_URL = '/no_trailing_slash'

        with self.assertRaises(ImproperlyConfigured):
            self.app.settings.STATIC_URL = '/no_trailing_slash'

        self.app.settings.MEDIA_URL = '/with_trailing_slash/'