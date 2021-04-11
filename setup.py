
from setuptools import setup, find_packages


setup(
    name='sampleproject',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Deployment test project for AWS',
    author='Tyler Ryu',
    author_email='tylerk.ryu@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ]
)