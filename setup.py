from setuptools import setup

setup(
    name='nolog',
    version='0.0.1',
    description='Python interface for NoLog',
    url="git@github.com:nolog-io/nolog-python-lib.git",
    author="NoLog",
    author_email="nolog-python-client@nolog.io",
    license='unlicensed',
    packages=['nolog', 'nolog.generated.source.proto.main.python.write', 'nolog.generated.source.proto.main.python.auth'],
    zip_safe=True,
    install_requires=[
        'protobuf'
    ],
)
