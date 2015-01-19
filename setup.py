from setuptools import setup

setup(
    name='tidytex',
    version='0.1',
    description='Compile LaTeX with no auxiliary files',
    long_description='''
    Continuously compile LaTeX, keeping auxiliary files in a temporary
    folder, which is destroyed when the process is killed.
    ''',
    author='Colin Carroll',
    py_modules=['tidytex'],
    url='https://github.com/ColCarroll/tidytex',
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
