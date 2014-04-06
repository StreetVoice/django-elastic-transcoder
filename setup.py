from setuptools import setup, find_packages
from dj_elastictranscoder import __version__


setup(
    name='django-elastic-transcoder',
    version=__version__,
    description="django-elastic-transcoder",
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
