from setuptools import setup
import subprocess

version = subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"]).strip().decode()

assert version[0] == "v"  # Something went wrong

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="python-tkdnd",
    version=version,
    description="Native drag & drop capabilities in tkinter. The tkinterDnD package is a nice and easy-to-use wrapper around the tkdnd tcl package.",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/tkinterDnD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ttkwidgets >= 0.11.0"],
    python_requires=">=3.6",
    license="MIT license",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["tkinterDnD"],
    package_data={"tkinterDnD": ["windows/*", "linux/*", "mac/*"]}
)
