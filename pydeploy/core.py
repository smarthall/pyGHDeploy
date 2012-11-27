import json, yaml, os
import actions

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
    # Load the JSON payload
    data = json.loads(payload)

    # Count files changed
    added = []
    modified = []
    removed = []
    for commit in data['commits']:
      added.extend(commit['added'])
      modified.extend(commit['modified'])
      removed.extend(commit['removed'])

    # Make summary
    summary = {
        'name': data['repository']['name'],
        'url': data['repository']['url'],
        'added': list(set(added)),
        'modified': list(set(modified)),
        'removed': list(set(removed))
    }

    # Call plugins
    for repo in self.config['githubrepo']:
      if repo['name'] == data['repository']['name']:
        plug = getattr(actions, repo['action'])
        print plug(summary)

    # Output
    return "ok.\n"
  github.exposed = True

