import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
    name="productivity-tracker",
    version="0.0.2",
    description="Command-line utility for tracking time spent on projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nikita Toropov",
    author_email="toropov.nikita2004@gmail.com",
    url="https://github.com/tossik8/tracker",
    license="MIT",
    keywords="tracker,time-tracker,productivity",
    entry_points={
        "console_scripts": [
            "tracker = productivity_tracker.main:main"
        ]
    },
    python_requires=">=3.12"
)