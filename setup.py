import os
import sys

from setuptools import setup, find_packages


def get_version():
    code = None
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'dj_elastictranscoder',
        '__init__.py',
    )
    with open(path) as f:
        for line in f:
            if line.startswith('__version__'):
                code = line[len('__version__ = '):]
                break
    return eval(code)


if sys.argv[-1] == 'wheel':
    os.system('pip wheel --wheel-dir=wheelhouse .')
    sys.exit()

setup(
    name='django-elastic-transcoder',
    version=get_version(),
    description="Django with AWS elastic transcoder",
    long_description=open('README.rst').read(),
    author='tzangms',
    author_email='tzangms@streetvoice.com',
    url='http://github.com/StreetVoice/django-elastic-transcoder',
    license='MIT',
    packages=find_packages(exclude=('testsapp', )),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "boto3 >= 1.1",
        "django >= 1.3, < 1.9",
        "qiniu >= 7.0.8",
        "south >= 0.8",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    keywords='django,aws,elastic,transcoder,qiniu,audio,aliyun',
)
