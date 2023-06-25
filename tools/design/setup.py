from setuptools import setup, find_packages

setup(name = "design",
    version = "0.0.1",
    description = "aircraft design tools",
    author = "Slade Brooks",
    author_email = "spbrooks4@gmail.com",
    packages = find_packages(),
    install_requires = ["numpy", "matplotlib", "pandas"],
)