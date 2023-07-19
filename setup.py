from setuptools import setup, find_packages

setup(
    name='panda_power_tools',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests']),
    description='Package for work with PandaPower',
    install_requires=[],
    author = 'Viktar Yanush',
    author_email = 'vicjan89@gmail.com',
    license='MIT',
    long_description=open('README.md').read(),
)
