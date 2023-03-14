from setuptools import setup, find_packages

setup(
    name="FishHunterUtil",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "regex",
        "requests",
        "urllib3",
        "lxml",
        "tinycss",
        "beautifulsoup4",
        "json",
        "hashlib",
        "selenium",
        "webdriver_manager"
    ],
    author="I Kadek Agus Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    description="Packages to help fish-hunter.",
)