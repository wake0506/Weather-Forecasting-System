from setuptools import setup, find_packages

setup(
    name="weather-forecasting-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "requests>=2.28.0",
    ],
)
