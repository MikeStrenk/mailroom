import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mailroom-pkg",
    version="0.0.1",
    author="Michael Strenk",
    author_email="mikestrenk@gmail.com",
    description="Toolkit to generate & distribute html email reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MikeStrenk/mailroom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)