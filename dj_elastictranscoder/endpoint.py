import json

def handler(notification_type):
    filename = 'fixtures/on%s.json' % notification_type
    with open(filename) as f:
        data = json.loads(f.read())
        print data['Message']


handler('progress')
handler('error')
handler('complete')
