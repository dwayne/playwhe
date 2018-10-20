from setuptools import setup


setup(
    install_requires=['requests', 'sqlalchemy'],
    entry_points={
        'console_scripts': [
            'playwhe=playwhe.cli:main'
        ]
    }
)
