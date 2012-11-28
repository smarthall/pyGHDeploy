import json, yaml, os
import git
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
    print "\n\n\n\n"

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

    # Clone/update the repo
    repopath = "/tmp/" + data['repository']['name']
    if not os.path.exists(repopath):
        git.Git().clone(data['repository']['url'], repopath)

    repo = git.Repo(repopath)
    repo.git.reset('HEAD', hard=True)
    repo.git.pull(rebase=True)

    # Make summary
    summary = {
        'name': data['repository']['name'],
        'url': data['repository']['url'],
        'path': repopath,
        'repo': repo,
        'added': list(set(added)),
        'modified': list(set(modified)),
        'removed': list(set(removed))
    }

    # Call plugins
    for repo in self.config['githubrepo']:
      if repo['name'] == data['repository']['name']:
        self.callaction(summary, repo['action'], repo['args'])

    # Output
    return "ok.\n"
  github.exposed = True

  def callaction(self, summary, action, args):
    plug = getattr(actions, action)
    print plug(summary, args)
    

