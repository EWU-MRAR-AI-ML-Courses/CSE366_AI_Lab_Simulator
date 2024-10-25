# setup.py

from setuptools import setup, find_packages

setup(
    name='cse366_ai_lab_simulator',
    version='0.1.0',
    description='CSE 366 AI Lab Simulator Library',
    author='Md Rifat Ahmmad Rashid',
    author_email='rifat.rashid@ewubd.edu',
    url='https://github.com/your_username/CSE366_AI_Lab_Simulator',
    packages=find_packages(include=['modules', 'modules.*']),
    install_requires=[
        'pygame',
        # Add other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
