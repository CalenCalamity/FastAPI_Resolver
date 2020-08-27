from setuptools import setup, find_packages

version = '1.0.0'

setup(
    name='Resolver',
    version=version,
    description='The SAEON URL Resolver Service',
    url='https://github.com/SAEONData/FastAPI_Resolver',
    author='Lance Mac Donald',
    author_email='lance@saeon.ac.za',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='~=3.7',
    install_requires=[
        'fastapi',
        'sqlalchemy',
        'python-dotenv',
        'uvicorn',
        'psycopg2',
        'pytest'
    ],
    extras_require={
        'test': ['pytest', 'coverage']
    },
)
