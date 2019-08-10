from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Pacote para coletar e fazer métricas do Pizza',
    author='Pizza de Dados',
    author_email='pizzadedados@gmail.com',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)