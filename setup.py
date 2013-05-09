from setuptools import setup, find_packages
import stream

setup(
    name='django-stream',
    description='Activity stream application for Django',
    long_description=open('README.rst').read(),
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-stream',
    version=stream.__version__,
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(exclude=('tests*',)),
    package_data={'stream': ['templates/stream/*.html'],}
)
