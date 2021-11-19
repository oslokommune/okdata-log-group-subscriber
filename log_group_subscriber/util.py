import os


def getenv(name):
    """Return the environment variable named `name`, or raise OSError if unset."""
    env = os.getenv(name)

    if not env:
        raise OSError(f"Environment variable {name} is not set")

    return env
