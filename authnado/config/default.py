from os.path import abspath, dirname, join


def root(*paths):
    """
    The directory containing the "manage.py" script.
    """
    return join(dirname(dirname(abspath(__file__))), *paths)


settings = {
    'template_path': root('templates'),
    'thread_size': 4,
    'debug': False,
    'port': 8080,
}
