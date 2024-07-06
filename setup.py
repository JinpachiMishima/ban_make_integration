from setuptools import setup, find_packages

setup(
    name='ban_integration',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'sqlalchemy>=2.0.31',
    ],
    author='Advard Nigma',
    author_email='advard.nigma117@gmail.com',
    description='Library for make integration amocrm, wazzup',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8.0',
)
