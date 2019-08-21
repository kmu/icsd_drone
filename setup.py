#!/usr/bin/env python

import os

from setuptools import setup, find_packages

module_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    setup(
        name='icsd_drone',
        version="2019.08.21",
        description='',
        long_description=open(os.path.join(module_dir, 'README.md'),encoding='utf-8').read(),
        long_description_content_type="text/markdown",
        url='https://github.com/kmu/icsd_drone',
        author='Koki Muraoka',
        author_email='kmuroaka@lbl.gov',
        packages=find_packages(),
        include_package_data=True,
        package_data={},
        zip_safe=False,
        install_requires=[
            'pymatgen', 'emmet'
        ],
        classifiers=["Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.6",
                     'Intended Audience :: Science/Research',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering'],
        entry_points='''
        [console_scripts]
        icsd_drone=icsd_drone.scripts.emmet:cli
        ''',
        python_requires='>=3.6',
    )
