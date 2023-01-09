from setuptools import setup

setup(
    name='hetpy',
    version='0.1.0',
    description='A package to handle heterogeneous information networks',
    url='https://github.com/codingfabi/hetpy',
    author='Fabian Kneissl',
    author_email='fabian.kneissl@gmx.de',
    license='GNU General Public License',
    packages=['hetpy'],
    install_requires=['igraph']
)