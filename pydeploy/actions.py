import subprocess, os
import git, shutil

def argprint(summary, args):
  return summary

def command(summary, args):
  return subprocess.call(args)

def ansible(summary, args):
  repopath = "/tmp/" + hashlib.md5(args['ansiblerepo']).hexdigest()
  if not os.path.exists(repopath):
      git.Git().clone(args['ansiblerepo'], repopath)

  repo = git.Repo(repopath)
  repo.git.reset('HEAD', hard=True)
  repo.git.pull(rebase=True)

  result = subprocess.call(['/usr/bin/ansible-playbook',
                           repopath + "/" + args['filename']])
  return result

