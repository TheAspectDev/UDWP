from setuptools import setup, find_packages

setup(
    name='udwp',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "websockets", "asyncio", "requests"
    ],
)