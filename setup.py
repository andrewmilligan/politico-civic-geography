from setuptools import find_packages, setup

from geography import __version__

setup(
    name="politico-civic-geography",
    version=__version__,
    description="",
    url="https://github.com/The-Politico/politico-civic-geography",
    author="POLITICO interactive news",
    author_email="interactives@politico.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="",
    include_package_data=True,
    packages=find_packages(exclude=["docs", "tests", "example"]),
    install_requires=[
        "boto3",
        "census",
        "DictObject",
        "django",
        "djangorestframework",
        "dj-database-url",
        "geojson",
        "psycopg2",
        "pyshp",
        "shapely",
        "stringcase",
        "tqdm",
        "us",
    ],
    extras_require={
        "dev": ["sphinx", "sphinxcontrib-django", "sphinx-rtd-theme"],
        "test": ["pytest"],
    },
)
