from setuptools import setup, find_packages

setup(
    name = "mlops",
    version = 0.1,
    install_requires = ["azureml-core"],
    packages = find_packages()
)
