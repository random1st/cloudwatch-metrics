import os

from setuptools import setup, find_packages

from cloudwatch_metrics.version import VERSION

with open(os.path.join(os.path.dirname(__file__),
                       'README.md')) as readme:
    README = readme.read()

setup(
    name='cloudwatch_metrics',
    version=VERSION,
    description='The Cloudwatch Metrics package enables Python developers to record'
                ' and emit information from within their applications to the Cloudwatch service.',
    long_description=README,
    long_description_content_type='text/markdown',

    url='https://github.com/random1st/cloudwatch-metrics',
    author='Amazon Web Services',
    license="GPLv3",

    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    install_requires=[
        'aiobotocore',
        'boto3<=1.16.52',
        'async-property'
    ],

    keywords='aws cloudwatch metrics',

    packages=find_packages(exclude=['tests*']),
    include_package_data=True
)
