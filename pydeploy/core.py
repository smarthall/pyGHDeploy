import json, yaml, os

class Server:
  def __init__(self):
    # Process the config
    if os.path.exists('/etc/pydeploy.yaml'):
      config = yaml.safe_load(open('/etc/pydeploy.yaml','r'))
    else:
      config = yaml.safe_load(open('conf/default.yaml','r'))

  def index(self):
    return "Hello world!"
  index.exposed = True

  def github(self, payload=None):
    added = []
    modified = []
    removed = []
    data = json.loads(payload)
    for commit in data['commits']:
      added.extend(commit['added'])
      modified.extend(commit['modified'])
      removed.extend(commit['removed'])
      reply = {
          'name': data['repository']['name'],
          'added': added,
          'modified': modified,
          'removed': removed
      }
    message = json.dumps(reply, sort_keys=True, indent=4) + "\n"
    return message
  github.exposed = True

