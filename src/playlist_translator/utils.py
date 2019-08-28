import os


def get_environ(var_name):
    """
    Lookup an environment variable and return it's value. Raise an error
    if it doesn't exist.
    """
    var = os.environ.get(var_name)
    if var is None:
        msg = 'Missing required environment variable "{}"'.format(var_name)
        raise OSError(msg)
    return var
