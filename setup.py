from setuptools import setup

setup(
    name='tidytex',
    version='0.1',
    py_modules=['tidytex'],
    include_package_data=True,
    install_requires=[
        'Click',
        'pexpect',
    ],
    entry_points='''
        [console_scripts]
        tidytex=tidytex:tidy
    ''',
)