Django Elastic Transcoder
=========================

|Build Status| |Coverage Status|

``django-elastic-transcoder`` is an `Django` app, let you integrate AWS Elastic Transcoder in Django easily.

What is provided in this package?

- ``Transcoder`` class
- URL endpoint for receive SNS notification
- Signals for PROGRESS, ERROR, COMPLETE
- ``EncodeJob`` model

Workflow
-----------

.. image:: https://github.com/StreetVoice/django-elastic-transcoder/blob/master/docs/images/workflow.jpg


Install
-------

First, install ``dj_elastictranscode`` with ``pip``

.. code:: sh

    $ pip install django-elastic-transcoder

Then, add ``dj_elastictranscoder`` to ``INSTALLED_APPS``

.. code:: python

    INSTALLED_APPS = (
        ...
        'dj_elastictranscoder',
        ...
    )

Bind ``urls.py``

.. code:: python

    urlpatterns = patterns('',
        ...
        url(r'^dj_elastictranscoder/', include('dj_elastictranscoder.urls')),
        ...
    )

Migrate

.. code:: sh

    $ ./manage.py migrate

Setting up AWS Elastic Transcoder
---------------------------------

1. Create a new ``Pipeline`` in AWS Elastic Transcoder.
2. Hookup every Notification.
3. Subscribe SNS Notification through HTTP
4. You are ready to encode!


Required Django settings
-------------------------

Please settings up variables below to make this app works.

.. code:: python

    AWS_ACCESS_KEY_ID = <your aws access key id>
    AWS_SECRET_ACCESS_KEY = <your aws secret access key>
    AWS_REGION = <aws region>

Usage
-----

For instance, encode an mp3

.. code:: python

    from dj_elastictranscoder.transcoder import Transcoder

    input = {
        'Key': 'path/to/input.mp3', 
    }

    outputs = [{
        'Key': 'path/to/output.mp3',
        'PresetId': '1351620000001-300040' # for example: 128k mp3 audio preset
    }]

    pipeline_id = '<pipeline_id>'

    transcoder = Transcoder(pipeline_id)
    transcoder.encode(input, outputs)

    # your can also create a EncodeJob for object automatically
    transcoder.create_job_for_object(obj)


    # Transcoder can also work standalone without Django
    # just pass region and required aws key/secret to Transcoder, when initiate

    transcoder = Transcoder(pipeline_id, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


Setting Up AWS SNS endpoint
---------------------------------

AWS Elastic Transcoder can send various SNS notification to notify your application, like ``PROGRESS``, ``ERROR``, ``WARNING`` and ``COMPLETE``

So this package provide a endpoint to receive these notifications, for you to update transcode progress. without checking by your self.

Go to SNS section in AWS WebConsole to choose topic and subscribe with the url below.

``http://<your-domain>/dj_elastictranscoder/endpoint/``

Before notification get started to work, you have to activate SNS subscription, you will receive email with activation link.

After subscribe is done, you will receive SNS notification.

    
Signals
-----------

This package provide various signals for you to get notification, and do more things in your application. you can check the signals usage in tests.py for more usage example.

* transcode_onprogress
* transcode_onerror
* transcode_oncomplete


.. |Build Status| image:: https://travis-ci.org/StreetVoice/django-elastic-transcoder.png?branch=master
   :target: https://travis-ci.org/StreetVoice/django-elastic-transcoder
.. |Coverage Status| image:: https://coveralls.io/repos/StreetVoice/django-elastic-transcoder/badge.png?branch=master
   :target: https://coveralls.io/r/StreetVoice/django-elastic-transcoder?branch=master
