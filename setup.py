from setuptools import setup, find_packages

setup(
    name="FishHunterUtil",
    version="1.2.8",
    packages=find_packages(),
    install_requires=[
        "regex",
        "requests",
        "urllib3",
        "lxml",
        "tinycss",
        "beautifulsoup4",
        "selenium",
        "webdriver_manager",
        "scikit-learn",
        "ngram",
        "numpy",
        "tldextract",
        "python-whois",
    ],
    author="I Kadek Agus Ariesta Putra",
    author_email="ikadekagusariestaputra@gmail.com",
    description="Packages to help fish-hunter.",
)