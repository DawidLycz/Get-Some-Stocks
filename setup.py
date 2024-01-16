from setuptools import setup, find_packages

setup(
    name='GetSomeStocks',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
