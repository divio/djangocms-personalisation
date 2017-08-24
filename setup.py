# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from djangocms_segmentation import __version__


setup(
    name='djangocms-segmentation',
    version=__version__,
    description='Visitor Segmentation for django CMS',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/divio/djangocms-segmentation',
    packages=find_packages(),
    package_data={},
    license='LICENSE.txt',
    platforms=['OS Independent'],
    install_requires=[
        'django-cms>=3.5',
        'Django>=1.8',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
    zip_safe=False
)
