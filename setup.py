from setuptools import setup
from dj_elastictranscoder import __version__


setup(
    name='django-elastic-transcoder',
    version=__version__,
    description="Django with AWS elastic transcoder",
    long_description=open("README.rst").read(),
    author='tzangms',
    author_email='tzangms@streetvoice.com',
    url='http://github.com/StreetVoice/django-elastic-transcoder',
    license='MIT',
    test_suite='runtests.runtests',
    packages=['dj_elastictranscoder',],
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        "django >= 1.4",
        "boto >= 2.5",
        "South >= 0.8",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django,aws,elastic,transcoder',
)
