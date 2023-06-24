from setuptools import setup, find_packages

setup(name = "utils",
    version = "0.0.1",
    description = "engineering utils package",
    author = "Slade Brooks",
    author_email = "spbrooks4@gmail.com",
    packages = find_packages(),
    install_requires = ["numpy"],
)