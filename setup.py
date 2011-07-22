from setuptools import setup, find_packages

setup(
    name='django-stream',
    description='Activity stream application for Django',
    long_description=open('README.rst').read(),
    packages=['stream', 'stream.templatetags'],
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-stream',
    version='0.2',
    include_package_data=True,
    zip_safe=False,
    package_data={'stream': ['templates/stream/*.html'], }
)
