from setuptools import setup, find_packages

setup(
    name='chatbot',
    version='0.1',
    author='Czellár Botond',
    author_email='czellar.botond@email.com',
    description='Messenger Chat Bot',
    packages=find_packages(),
    install_requires=[
        'requests',
        'flask',
        'selenium',
        'pymessenger',
        'beautifulsoup4',
    ],
)