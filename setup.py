from setuptools import setup, find_packages

setup(
    name="verbo",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'verbo = src.main:main',  # Adjust if `main.py` has a main() function
        ],
    },
    install_requires=[
        # Add your dependencies here, e.g.,
        # 'numpy', 'requests',
    ],
)
