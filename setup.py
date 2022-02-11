from setuptools import setup, find_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Needed for dependencies
INSTALL_REQUIRES = [    'pandas',
                        'numpy',
                        'matplotlib',
                        'pyodbc',
                        'inference-tools',
                        'azure.storage.blob'    ]

CLASSIFIERS = [ 'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
                'Intended Audience :: Developers',      # Define that your audience are developers
                'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: MIT License',   # Again, pick a license
                'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
                'Programming Language :: Python :: 3.7' ]

setup(  name='multitools',
        version='0.0.1',
        url='https://github.com/dgahle/OmniTools',
        download_url="https://github.com/dgahle/OmniTools/archive/refs/tags/v0.0.1.tar.gz",
        packages=find_packages(include=['multitools']),
        license='MIT License',
        author='Daljeet Singh Gahle',
        description='A general repo for data processing and statistical analysis tools in Python.',
        long_description_content_type='text/markdown',
        long_description=long_description,
        install_requires=INSTALL_REQUIRES,
        python_requires='>=3.7',
        zip_safe=False,
        keywords=['data analysis', 'data processing', 'statistics', 'pandas support'],  # Keywords that define your package best
        classifiers=CLASSIFIERS   )

