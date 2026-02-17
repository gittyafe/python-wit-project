from setuptools import setup


setup(
    name='wit',
    version='0.1.0',
    py_modules=['click_wit', 'wit_defs', 'helper_files'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'wit = click_wit:cli',  
        ],
    },
)