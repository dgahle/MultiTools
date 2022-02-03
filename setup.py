from setuptools import setup, find_packages

setup(
    name='omnitools',
    version='0.0.1',
    packages=find_packages(include=['omnitools']),
    license='MIT License',
    author='Daljeet Singh Gahle',
    description='A general repo for data processing and statistical analysis tools in Python.',
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'pyodbc',
        'inference-tools',
        'azure.storage.blob' ]
    )