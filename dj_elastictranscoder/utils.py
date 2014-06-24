from django.utils.text import slugify

from .transcoder import Transcoder


def et_create_job(job):
    if not job.output:
        outputs = [{
            'Key': 'outputs/%s.mp4' % slugify(unicode(job)),
            'PresetId': job.preset
        }]

        transcoder = Transcoder(job.pipeline_id)
        transcoder.encode({'Key': job.upload.video.name}, outputs)
        job.et_job_id = transcoder.create_job_for_object(job)
        job.save(update_fields=['et_job_id'])


def et_read_job(job):
    transcoder = Transcoder(job.pipeline_id)
    et = transcoder.get_et()
    data = et.read_job(job.et_job_id)
    for output in data['Job']['Outputs']:
        if output['Status'] == 'Complete':
            job.output = output['Key']
            job.save(update_fields=['output'])
