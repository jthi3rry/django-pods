import unittest

import django
from django.apps import apps
from django.conf import settings

from pods.apps import AppSettings, AppSettingsHolder, underscore_capitalized

settings.configure(
    INSTALLED_APPS=[
        'tests.mocks'
    ],
    MOCK={
        "OTHER_APP_VARIABLE": "my_other_value"
    }
)

django.setup()


class TestAppSettings(unittest.TestCase):

    def setUp(self):
        self.app = apps.get_app_config('mocks')

    def test_has_settings(self):
        self.assertTrue(hasattr(self.app, 'settings'))
        self.assertTrue(hasattr(self.app.__class__, 'settings'))
        self.assertIsInstance(self.app.settings, AppSettingsHolder)

    def test_variables(self):
        from tests.mocks import app_test_settings
        self.assertEqual(self.app.settings.APP_VARIABLE, app_test_settings.APP_VARIABLE)

    def test_settings_override(self):
        from tests.mocks import app_test_settings
        self.assertNotEqual(self.app.settings.OTHER_APP_VARIABLE, app_test_settings.OTHER_APP_VARIABLE)
        self.assertEqual(self.app.settings.OTHER_APP_VARIABLE, "my_other_value")

    def test_imports(self):
        from tests.mocks import app_test_imports
        self.assertEqual(self.app.settings.APP_MODULE, app_test_imports.TestClass)

    def test_multiple_imports(self):
        from tests.mocks import app_test_imports
        self.assertListEqual(self.app.settings.MULTIPLE_APP_MODULES, [app_test_imports.TestClass, app_test_imports.OtherTestClass])

    def test_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.app.settings.DOES_NOT_EXIST

    def test_import_error(self):
        with self.assertRaises(ImportError):
            self.app.settings.NON_EXISTENT_APP_MODULE

    def test_settings_import_error(self):
        with self.assertRaises(ImportError):
            AppSettingsHolder("doesnotexist", "KEY")

    def test_default_settings_key_capitalizer(self):
        self.assertEqual(underscore_capitalized("MockAppConfig"), "MOCK_APP_CONFIG")
        self.assertEqual(underscore_capitalized("MockWithNumber1"), "MOCK_WITH_NUMBER_1")
        self.assertEqual(underscore_capitalized("RockNRollConfig"), "ROCK_N_ROLL_CONFIG")

    def test_settings_proxy(self):
        self.assertTrue(hasattr(self.app, 'APP_VARIABLE'))
        self.assertFalse(hasattr(self.app, 'DOES_NOT_EXIST'))

    def test_without_django_apps_framework(self):

        class SettingsEnabledClass(AppSettings):
            settings_key = 'MOCK'
            settings_module = 'tests.mocks.app_test_settings'

        app = SettingsEnabledClass()
        self.assertTrue(hasattr(app, 'settings'))
        self.assertTrue(hasattr(app.__class__, 'settings'))
        self.assertIsInstance(app.settings, AppSettingsHolder)
