DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'dj_elastictranscoder',
    'testsapp',
]
SITE_ID = 1
DEBUG = False
ROOT_URLCONF = ''
SECRET_KEY='test'