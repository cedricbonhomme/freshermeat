
import sys
import subprocess

from bootstrap import application

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in application['ALLOWED_EXTENSIONS']


def import_github(owner=None, repo=None):
    cmd = [sys.executable, application.config['HERE'] + '/src/manager.py',
            'import_project_from_github',
            owner, repo]
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return stdout
