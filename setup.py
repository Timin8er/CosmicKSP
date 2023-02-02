"""the install script for Cosmic KSP"""
from setuptools import setup, find_packages


setup(
    name='CosmicKSP',
    version='1.0',
    description='Cosmos to KSP commands and telemetry',
    author='Tim Polnow',
    author_email='',
    url='https://github.com/Timin8er/CosmicKSP',
    packages=find_packages(),
    zip_safe=False,
    package_data={'CosmicKSP.kos_scripts': ['*.ks']},
    install_requires=[
        'PyQt5',
        'websocket-client',
        # 'telnetlib',
        'pyyaml',
        'keyboard',
        ],
    entry_points={
            'console_scripts': [
                'CosmicRelay = CosmicRelay:main',
                'CosmicRelay_Telemetry = CosmicRelay.telemetry_relay:main',
                'CosmicRelay_Commanding = CosmicRelay.commands_relay:main',
                'CosmicGameManager = CosmicGameManager:main',
            ]
        }
    )
