from os import path

from setuptools import setup, find_packages

from cloudwatch_metrics.version import VERSION

CURRENT_DIR = path.abspath(path.dirname(__file__))

long_description = read_md(path.join(CURRENT_DIR, 'README.md'))

setup(
    name='cloudwatch_metrics',
    version=VERSION,

    description='The Cloudwatch Metrics package enables Python developers to record'
                ' and emit information from within their applications to the Cloudwatch service.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/random1st/cloudwatch-metrics',

    author='Amazon Web Services',

    license="GPLv3",

    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: GPLv3 :: GNU Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    install_requires=[
        'boto3',
        'aibotocore',
    ],

    keywords='aws cloudwatch metrics',

    packages=find_packages(exclude=['tests*']),
    include_package_data=True
)
