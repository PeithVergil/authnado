from os.path import abspath, dirname, join


def root(*paths):
    """
    The directory containing the "manage.py" script.
    """
    return join(dirname(dirname(abspath(__file__))), *paths)


settings = {
    'template_path': root('templates'),
    'static_path': root('assets'),
    'threads': 4,
    'debug': False,
    'port': 8080,
}
