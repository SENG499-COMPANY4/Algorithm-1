from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Algorithm-1',
   version='1.0',
   description='An API for company 4 sechduling algorithm',
   long_description=long_description,
   author='Jesse Lacroix',
   author_email='jesselacroix@uvic.ca',
   packages=['Algorithm-1'],  #same as name
   install_requires=['flask'],
   scripts=[
            
           ]
)