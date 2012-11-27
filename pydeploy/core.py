import json, yaml, os
import plugins

class Server:
  def __init__(self):
    # Process the config
    if os.path.exists('/etc/pydeploy.yaml'):
      self.config = yaml.safe_load(open('/etc/pydeploy.yaml','r'))
    if os.path.exists('conf/local.yaml'):
      self.config = yaml.safe_load(open('conf/local.yaml','r'))
    else:
      self.config = yaml.safe_load(open('conf/default.yaml','r'))

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
        'url': data['repository']['url'],
        'added': list(set(added)),
        'modified': list(set(modified)),
        'removed': list(set(removed))
    }
    for repo in self.config['githubrepo']:
      if repo['name'] == data['repository']['name']:
        reply['action'] = repo['action']
        plug = getattr(plugins, repo['action']['name'])
        plug(reply)

    message = json.dumps(reply, sort_keys=True, indent=4) + "\n"
    message += json.dumps(self.config, sort_keys=True, indent=4) + "\n"
    return message
  github.exposed = True

