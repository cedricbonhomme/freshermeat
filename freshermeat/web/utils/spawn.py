import os
import subprocess
import sys

from freshermeat.bootstrap import application

ERRORS = {
    "ERROR:DUPLICATE_NAME": "A project with this name already exists.",
    "ERROR:NO_LICENSE": "No license found.",
    "ERROR:OBSCURE": "An obscure error occurred.",
}


def import_github(repository, submitter_id=None):
    print("test")
    owner, repo = repository.split("/")[-2:]
    env = os.environ.copy()
    env["FLASK_APP"] = "runserver.py"
    cmd = [
        sys.exec_prefix + "/bin/flask",
        "import_project_from_github",
        "--owner",
        owner,
        "--repo",
        repo,
        "--submitter_id",
        str(submitter_id),
    ]
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    (stdout, stderr) = p.communicate()
    return stdout


def import_gitlab(repository, submitter_id=None):
    cmd = [
        sys.executable,
        application.config["HERE"] + "/manager.py",
        "import_project_from_gitlab",
        repository,
        str(submitter_id),
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return stdout
