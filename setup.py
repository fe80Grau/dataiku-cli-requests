from setuptools import setup, find_packages

setup(
    name='dataiku-cli-requests',
    version='1.0',
    url='https://www.funiber.org',
    author='David Grau Martinez',
    author_email='david.grau@funiber.org',
    description='Una herramienta de línea de comandos para interactuar con Dataiku utilizando solicitudes HTTP',
    packages=find_packages(),
    install_requires=[
        'requests',
        'argparse',
        'more-itertools>=8.12.0',
    ],
    entry_points={
        'console_scripts': [
            'dataiku-cli-requests=dataiku_cli_requests.dataiku_cli_requests:main',
        ],
    },
)
