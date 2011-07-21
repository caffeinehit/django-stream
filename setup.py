from setuptools import setup, find_packages

setup(
    name='django-stream',
    description='Application providing news stream like features on django models',
    packages=['stream'],
    author='Alen Mujezinovic',
    author_email='alen@caffeinehit.com',
    url='https://github.com/caffeinehit/django-stream',
    version='0.2',
    include_package_data=True,
    zip_safe=False,
    package_data={'stream': ['templates/stream/*.html'], }
)
