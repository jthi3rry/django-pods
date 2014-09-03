from pods.apps import AppSettings


class MockAppConfig(AppSettings):
    settings_key = 'MOCK'
    settings_module = 'tests.mocks.app_test_settings'
    settings_imports = (
        'APP_MODULE',
        'MULTIPLE_APP_MODULES',
        'NON_EXISTENT_APP_MODULE'
    )
