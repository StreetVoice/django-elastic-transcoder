from django.utils.text import slugify

from .transcoder import Transcoder


def et_create_job(job):
    qs = job.output_set.filter(video="")
    if qs.exists():
        outputs = []
        for output in qs:
            outputs.append({
                'Key': 'outputs/%s.mp4' % slugify(unicode(output)),
                'PresetId': output.preset
            })

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
            obj = job.output_set.get(preset=output['PresetId'])
            obj.video = output['Key']
            obj.save(update_fields=['video'])
