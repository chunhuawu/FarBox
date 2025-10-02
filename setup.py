#!/usr/bin/env python3
"""
FarBox Bucket - A content management and synchronization system
Optimized dependencies - only what's actually used.
"""
from setuptools import setup, find_packages
from farbox_bucket import version

# Core dependencies - verified as used in codebase
DEPENDENCIES = [
    # ============================================================================
    # Web Framework (72 imports)
    # ============================================================================
    "flask>=3.0.0,<4.0.0",          # Latest stable 3.x
    "jinja2>=3.1.0,<4.0.0",         # Template engine
    "werkzeug>=3.0.0,<4.0.0",       # WSGI utilities

    # ============================================================================
    # Async & Networking (29 imports)
    # ============================================================================
    "gevent>=24.2.0",               # Async I/O - latest
    "farbox-gevent-websocket",      # WebSocket support
    "dnspython>=2.6.0",             # DNS toolkit
    "requests>=2.32.0",             # HTTP library (9 imports)

    # ============================================================================
    # Database & Caching (3+2 imports)
    # ============================================================================
    "pyssdb>=0.4.2",                # SSDB client
    "elasticsearch>=8.14.0,<9.0.0", # Search engine client
    "pymemcache>=4.0.0",            # Memcached client

    # ============================================================================
    # Security & Encryption (4+3 imports)
    # ============================================================================
    "cryptography>=42.0.0",         # Modern crypto (replaces pycrypto)
    "pyopenssl>=24.1.0",            # OpenSSL bindings
    "itsdangerous>=2.2.0",          # Signing/tokens

    # ============================================================================
    # Data Processing (13 imports)
    # ============================================================================
    "ujson>=5.10.0",                # Fast JSON
    "python-dateutil>=2.9.0",       # Date parsing
    "xmltodict>=0.13.0",            # XML parsing
    "unidecode>=1.3.0",             # Unicode to ASCII

    # ============================================================================
    # Image Processing
    # ============================================================================
    "pillow>=10.4.0",               # Image manipulation

    # ============================================================================
    # Markdown & Templates (4 imports each)
    # ============================================================================
    "farbox-markdown",              # Custom markdown processor
    "farbox-misaka",                # Fast markdown parser
    "pyjade>=4.0.0",                # Jade template support
    "pyscss>=1.4.0",                # SCSS compiler

    # ============================================================================
    # Cloud Storage (2 imports each)
    # ============================================================================
    "cos-python-sdk-v5>=1.9.0",     # Tencent Cloud (qcloud_cos)
    "boto3>=1.34.0",                # AWS S3

    # ============================================================================
    # Utilities (2 imports)
    # ============================================================================
    "blinker>=1.8.0",               # Signal/event system
    "psutil>=6.0.0",                # System monitoring
    "shortuuid>=1.0.0",             # Short UUIDs
    "Send2Trash>=1.8.0",            # Safe file deletion

    # ============================================================================
    # Error Tracking
    # ============================================================================
    "sentry-sdk>=2.8.0",            # Modern Sentry (replaces raven)

    # ============================================================================
    # Deployment
    # ============================================================================
    "xserver",                      # Custom deployment tool
]

# Development dependencies
DEV_DEPENDENCIES = [
    # Testing
    "pytest>=8.2.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.14.0",

    # Code quality
    "black>=24.4.0",
    "ruff>=0.5.0",
    "isort>=5.13.0",
    "mypy>=1.10.0",

    # Development tools
    "ipython>=8.25.0",
    "ipdb>=0.13.0",
]

# Optional dependencies for specific features
EXTRAS = {
    'dev': DEV_DEPENDENCIES,
    'test': [
        "pytest>=8.2.0",
        "pytest-cov>=5.0.0",
    ],
    'wechat': [
        # WeChat integration dependencies (if any specific ones)
    ],
    'ipfs': [
        # IPFS dependencies (if any specific ones)
    ],
}

setup(
    name='farbox_bucket',
    version=version,
    description='FarBox Bucket - Content Management and Synchronization System',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    author='Hepochen',
    author_email='hepochen@gmail.com',
    url='https://github.com/farbox/farbox_bucket',
    license='MIT',

    # Package configuration
    packages=find_packages(exclude=['tests', 'tests.*', 'scripts']),
    include_package_data=True,
    zip_safe=False,

    # Python version
    python_requires='>=3.8,<4.0',

    # Dependencies
    install_requires=DEPENDENCIES,
    extras_require=EXTRAS,

    # Entry points
    entry_points={
        'console_scripts': [
            'farbox_bucket=farbox_bucket.console:main',
            'build_farbox_bucket=farbox_bucket.deploy.build.build_image:build_farbox_bucket_image_from_console',
            'update_deploy_farbox_bucket=farbox_bucket.deploy.deploy:update_deploy_farbox_bucket',
            'deploy_farbox_bucket=farbox_bucket.deploy.deploy:deploy_from_console',
            'farbox_bucket_upgrade=farbox_bucket.deploy.deploy:upgrade_farbox_bucket',
            'farbox_bucket_update_web=farbox_bucket.deploy.deploy:update_farbox_bucket_web',
            'farbox_bucket_restart_web=farbox_bucket.deploy.deploy:update_farbox_bucket_web',
            'farbox_bucket_restart_cache=farbox_bucket.deploy.deploy:restart_farbox_bucket_cache',
        ]
    },

    # Metadata
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='cms content-management flask markdown blog website',
    platforms=['linux', 'darwin'],

    # Additional metadata
    project_urls={
        'Documentation': 'https://github.com/farbox/farbox_bucket',
        'Source': 'https://github.com/farbox/farbox_bucket',
        'Tracker': 'https://github.com/farbox/farbox_bucket/issues',
    },
)
