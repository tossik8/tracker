from setuptools import setup, find_packages

name = "tracker"

setup(
    name=name,
    author="Nikita Toropov",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            f"{name} = src.main:main"
        ]
    }
)