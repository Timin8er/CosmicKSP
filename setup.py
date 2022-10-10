from setuptools import setup, find_packages


setup(
    name='CosmicKSP',
    version='0.0',
    description='Cosmos to KSP commands and telemetry',
    author='Tim Polnow',
    author_email='',
    url='https://github.com/Timin8er/CosmicKSP',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
            'console_scripts': [
                'CosmicRelay = CosmicRelay:main',
                'CosmicGameManager = CosmicGameManager:main',
            ]
        }
    )
