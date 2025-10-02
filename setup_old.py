#!/usr/bin/env python
# coding: utf8
"""
FarBox Bucket - A content management and synchronization system
"""
from setuptools import setup, find_packages
from farbox_bucket import version

# Modern dependency specifications - Python 3.8+
DEPENDENCIES = [
    # Core web framework
    "flask>=2.3.0,<4.0.0",
    "jinja2>=3.1.0,<4.0.0",
    "werkzeug>=2.3.0,<4.0.0",

    # Database and storage
    "pyssdb>=0.4.2",
    "elasticsearch>=8.12.0,<9.0.0",
    "pymemcache>=4.0.0",

    # Async and networking
    "gevent>=23.9.0",
    "dnspython>=2.4.0",
    "farbox-gevent-websocket",

    # Security and encryption
    "cryptography>=41.0.0",  # Replaced pycrypto
    "pyopenssl>=23.0.0",
    "itsdangerous>=2.1.0",

    # Data processing
    "ujson>=5.8.0",
    "python-dateutil>=2.8.0",
    "shortuuid>=1.0.0",
    "xmltodict>=0.13.0",
    "unidecode>=1.3.0",

    # Image processing
    "pillow>=10.0.0",

    # Template engines
    "pyjade>=4.0.0",
    "pyscss>=1.4.0",

    # Markdown processing
    "farbox-markdown",
    "farbox-misaka",

    # Cloud storage
    "cos-python-sdk-v5>=1.9.0",
    "boto3>=1.34.0",

    # Utilities
    "blinker>=1.7.0",
    "psutil>=5.9.0",
    "Send2Trash>=1.8.0",
    "raven>=6.10.0",  # Sentry client

    # Deployment
    "xserver",
]

pipfile_packages = DEPENDENCIES

# Development dependencies
DEV_DEPENDENCIES = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

setup(
    name='farbox_bucket',
    version=version,
    description='FarBox Bucket - Content Management and Synchronization System',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    author='Hepochen',
    author_email='hepochen@gmail.com',
    url='https://github.com/farbox/farbox_bucket',
    include_package_data=True,
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3.8',
    install_requires=pipfile_packages,
    extras_require={
        'dev': DEV_DEPENDENCIES,
        'test': ["pytest>=7.4.0", "pytest-cov>=4.1.0"],
    },
    entry_points={
        'console_scripts': [
            'farbox_bucket = farbox_bucket.console:main',
            'build_farbox_bucket = farbox_bucket.deploy.build.build_image:build_farbox_bucket_image_from_console',
            'update_deploy_farbox_bucket = farbox_bucket.deploy.deploy:update_deploy_farbox_bucket',
            'deploy_farbox_bucket = farbox_bucket.deploy.deploy:deploy_from_console',
            'farbox_bucket_upgrade = farbox_bucket.deploy.deploy:upgrade_farbox_bucket',
            'farbox_bucket_update_web = farbox_bucket.deploy.deploy:update_farbox_bucket_web',
            'farbox_bucket_restart_web = farbox_bucket.deploy.deploy:update_farbox_bucket_web',
            'farbox_bucket_restart_cache = farbox_bucket.deploy.deploy:restart_farbox_bucket_cache',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    platforms=['linux', 'darwin'],
)