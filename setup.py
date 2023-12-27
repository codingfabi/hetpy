from setuptools import setup

setup(
    name='hetpy',
    version='1.0.3',
    description='A package to handle heterogeneous information networks',
    url='https://github.com/codingfabi/hetpy',
    author='Fabian Kneissl',
    author_email='fabian.kneissl@gmx.de',
    license='GNU General Public License',
    packages=['hetpy', 'hetpy.models','hetpy.graphUtils','hetpy.utils','hetpy.exceptions','hetpy.enums'],
    install_requires=['python-igraph']
)