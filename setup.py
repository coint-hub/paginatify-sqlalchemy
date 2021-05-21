from setuptools import setup

setup(
    name='coint-paginatify-sqlalchemy',
    version='0.0.4',
    packages=['paginatify', 'paginatify_sqlalchemy'],
    zip_safe=False,
    install_requires=['sqlalchemy>=1.0.11']
)
