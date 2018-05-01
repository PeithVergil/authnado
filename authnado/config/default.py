from os.path import abspath, dirname, join


def root(*paths):
    """
    The directory containing the "manage.py" script.
    """
    return join(dirname(dirname(abspath(__file__))), *paths)


settings = {
    'cookie_secret': (
        'e71f0bd68da05029e35ebb540dec8a77'
        '20b8d0040cce2e9c25419e683f6270d6'
    ),
    'template_path': root('templates'),
    'static_path': root('assets'),
    'threads': 4,
    'debug': False,
    'port': 8080,
}
