import subprocess, os
import git, shutil

def argprint(summary, args):
  return summary

def command(summary, args):
  return subprocess.call(args)

def ansible(summary, args):
  repopath = "/tmp/ansiblerepo"
  if not os.path.exists(repopath):
      git.Git().clone(args['ansiblerepo'], repopath)

  repo = git.Repo(repopath)
  repo.git.reset('HEAD', hard=True)
  repo.git.pull(rebase=True)

  result = subprocess.call('/usr/bin/ansible-playbook',
                           repopath + "/" + args['filename'])
  
  shutil.rmtree(repopath)
  return result

