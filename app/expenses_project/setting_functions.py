import os
from django.core.exceptions import ImproperlyConfigured


def get_env_var(var_name, default=None, required=False):
    """Gets an environment variable or throws an exception if it doesn't exist."""
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(f"Environment variable {var_name} is not set!")
    return value
