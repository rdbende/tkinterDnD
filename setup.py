from setuptools import setup

setup(
    name="python-tkdnd",
    version="0.1",
    description="Native drag & drop capabilities in tkinter. tkinterDnD is a nice wrapper around the tkdnd tcl package.",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/tkinterDnD",
    python_requires='>=3.6',
    packages=["tkinterDnD"],
    package_data={"tkinterDnD": ["windows/*", "linux/*", "mac/*"]}
)
