import sys
import subprocess

from bootstrap import application

ERRORS = {
    'ERROR:DUPLICATE_NAME': 'A project with this name already exists.',
    'ERROR:NO_LICENSE': 'No license found.',
    'ERROR:OBSCURE': 'An obscure error occurred.'
}

def import_github(owner=None, repo=None):
    cmd = [sys.executable, application.config['HERE'] + '/src/manager.py',
            'import_project_from_github',
            owner, repo]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return stdout

def import_gitlab(owner=None, repo=None):
    cmd = [sys.executable, application.config['HERE'] + '/src/manager.py',
            'import_project_from_gitlab',
            owner, repo]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return stdout
