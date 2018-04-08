from .default import settings as default_settings

try:
    from .custom import settings as custom_settings
except ImportError:
    # Only use the default settings.
    settings = {**default_settings}
else:
    # Merge the default and custom settings.
    settings = {**default_settings, **custom_settings}
