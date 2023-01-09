from setuptools import setup

setup(
    name='hetpy',
    version='0.1.1b',
    description='A package to handle heterogeneous information networks',
    url='https://github.com/codingfabi/hetpy',
    author='Fabian Kneissl',
    author_email='fabian.kneissl@gmx.de',
    license='GNU General Public License',
    packages=['hetpy', 'hetpy.models','hetpy.graphUtils','hetpy.utils','hetpy.exceptions'],
    install_requires=['python-igraph']
)