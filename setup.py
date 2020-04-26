""""
Setup Script
"""


import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="bodybuilder-alexsanjoseph",  # Replace with your own username
    version="0.0.1",
    author="Alex Josephh",
    author_email="alexsanjoseph@gmail.com",
    description="A python port of the NPM Bodybuilder Package",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/alexsanjoseph/bodybuilder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
