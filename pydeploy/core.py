import json

class Server:
  def index(self):
    return "Hello world!"
  index.exposed = True

  def github(self, payload=None):
    added = []
    modified = []
    removed = []
    data = json.loads(payload)
    message = json.dumps(data, sort_keys=True, indent=4) + "\n"
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
    message += json.dumps(reply, sort_keys=True, indent=4) + "\n"
    message += "ok.\n"
    return message
  github.exposed = True

