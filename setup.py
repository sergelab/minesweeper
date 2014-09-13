
from setuptools import setup, find_packages

setup_args = dict(
    name = 'minesweeper',
    version = '0.1',
    author = 'Brandproduction Ltd.',
    author_email = 'info@brpr.ru',
    url = '',
    description = 'Flask minesweeper project',
    long_description = open('README').read(),
    install_requires = [
        'setuptools',
        'zc.buildout',
    ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe = True
)

if __name__ == '__main__':
    setup(**setup_args)

