from setuptools import setup
setup(
    packages=["sdist_shiny"],
    name='sdist_shiny',
    install_requires=[
        "shiny",
        "pandas",
        "numpy",
        "seaborn"],
    dependency_links=["https://github.com/simonharnqvist/DISMaL.git#egg=dismal"],
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'sdist-shiny=sdist_shiny.run_app:main'
        ]
    }
)