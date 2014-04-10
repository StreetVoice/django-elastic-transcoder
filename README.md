django-elastic-transcoder
=========================

[![Build Status](https://travis-ci.org/StreetVoice/django-elastic-transcoder.png?branch=master)](https://travis-ci.org/StreetVoice/django-elastic-transcoder)
[![Coverage Status](https://coveralls.io/repos/StreetVoice/django-elastic-transcoder/badge.png?branch=master)](https://coveralls.io/r/StreetVoice/django-elastic-transcoder?branch=master)

Django + AWS Elastic Transcoder


Install
-----------

First, install `dj_elastictranscode` with `pip`

```sh
$ pip install django-elastic-transcoder
```

Then, add `dj_elastictranscoder` to `INSTALLED_APPS`


```python
INSTALLED_APPS = (
    ...
    'dj_elastictranscoder',
    ...
)
```

Bind `urls.py`

```python
urlpatterns = patterns('',
    ...
    url(r'^dj_elastictranscoder/', include('dj_elastictranscoder.urls')),
    ...
)
```

Migrate


```sh
$ ./manage.py migrate
```



Setting up AWS Elastic Transcoder
----------------------------------

1. Create a new `Pipeline` in AWS Elastic Transcoder.
2. Hookup every Notification. 
3. Subscribe SNS Notification through HTTP
4. You are ready to encode!



Usage
------------

For instance, encode an mp3

```python
from dj_elastictranscoder.transcoder import Transcoder

input = {
    'Key': 'path/to/input.mp3', 
}

outputs = [{
    'Key': 'path/to/output.mp3',
    'PresetId': '1351620000001-300040' # for example: 128k mp3 audio preset
}]

pipeline_id = '<pipeline_id>'

transcoder = Transcoder(pipeline_id, 'ap-southeast-1')
transcoder.encode(input, outputs)
```
