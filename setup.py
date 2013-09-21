from distutils.core import setup

setup(
    name='superscan',
    version='0.1',
    description='scans amazingly',
    author='Hannes Struss',
    author_email='x@hannesstruss.de',
    url='http://hannesstruss.de',
    py_modules=['superscan'],
    entry_points={
        'console_scripts': [
            'superscan = superscan:main',
        ],
    },
)
