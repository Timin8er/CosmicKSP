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
    install_requires=[
        'PyQt5',
        'websocket-client',
        ],
    entry_points={
            'console_scripts': [
                'CosmicRelay = CosmicRelay:main',
                'CosmicRelayDownlink = CosmicRelay:down_main',
                'CosmicRelayUplink = CosmicRelay:up_main',
                # 'CosmicConfig = CosmicKSP:main',
                'CosmicGameManager = CosmicGameManager:main',
            ]
        }
    )
