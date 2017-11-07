#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    dodo.py
'''

import os
import pwd

from utils.format import fmt

DIR = os.path.dirname(os.path.abspath(__file__))
UID = os.getuid()
GID = pwd.getpwuid(UID).pw_gid
USER = pwd.getpwuid(UID).pw_name
ENV = dict(AC_UID=UID, AC_GID=GID, AC_USER=USER)

LOG_LEVELS = [
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]

DOIT_CONFIG = {
    'default_tasks': ['pull', 'deploy', 'count'],
    'verbosity': 2,
}

ENVS = ' '.join([
    'PYTHONPATH=.:api:$PYTHONPATH',
])

class UnknownPkgmgrError(Exception):
    '''
    UnknownPkgmgrError
    '''
    def __init__(self):
        '''
        __init__
        '''
        super(UnknownPkgmgrError, self).__init__('unknown pkgmgr!')

def check_hash(program):
    '''
    check_hash
    '''
    from subprocess import check_call, CalledProcessError, PIPE
    try:
        check_call(fmt('hash {program}'), shell=True, stdout=PIPE, stderr=PIPE)
        return True
    except CalledProcessError:
        return False

def find_pyfiles(pattern='**/*.py', recursive=True):
    '''
    find_pyfiles
    '''
    from glob import glob
    return glob(pattern, recursive=recursive)

def task_count():
    '''
    use the cloc utility to count lines of code
    '''
    excludes = [
        'dist',
        'venv',
        '__pycache__',
        'auto_cert_cli.egg-info',
    ]
    excludes = '--exclude-dir=' + ','.join(excludes)
    scandir = os.path.dirname(__file__)
    return {
        'actions': [
            fmt('cloc {excludes} {scandir}'),
        ],
        'uptodate': [
            lambda: not check_hash('cloc'),
        ],
    }

def task_noroot():
    '''
    make sure script isn't run as root
    '''
    then = 'echo "   DO NOT RUN AS ROOT!"; echo; exit 1'
    bash = 'if [[ $(id -u) -eq 0 ]]; then {0}; fi'.format(then)
    return {
        'actions': [
            'bash -c \'{0}\''.format(bash),
        ],
    }

def task_pull():
    '''
    do a safe git pull
    '''
    test = '`git diff-index --quiet HEAD --`'
    pull = 'git pull --rebase'
    dirty = fmt('echo "refusing to \'{pull}\' because the tree is dirty"')
    return {
        'actions': [
            fmt('if {test}; then {pull}; else {dirty}; exit 1; fi'),
        ],
    }

def task_lint():
    '''
    run pylint
    '''
    for pyfile in find_pyfiles():
        yield {
            'name': pyfile,
            'actions': [
                fmt('pylint --rcfile .rcfile {pyfile}'),
            ],
        }

def task_test():
    '''
    setup venv and run pytest
    '''
    return {
        'task_dep': [
            'noroot',
        ],
        'actions': [
            'echo "test"',
        ],
    }

def task_version():
    '''
    write git describe to VERSION file
    '''
    return {
        'actions': [
            'git describe | xargs echo -n > VERSION',
        ],
    }

def task_deploy():
    '''
    deloy flask app via docker-compose
    '''
    return {
        'task_dep': [
            'noroot',
            'version',
            'test',
        ],
        'actions': [
            'echo "deploy"',
        ],
    }

def task_tidy():
    '''
    delete cached files
    '''
    TIDY_FILES = [
        '.doit.db/',
        'venv/',
        'api/VERSION',
    ]
    return {
        'actions': [
            'rm -rf ' + ' '.join(TIDY_FILES),
            'find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf', #pylint: disable=anomalous-backslash-in-string
        ],
    }

def task_nuke():
    '''
    git clean and reset
    '''
    return {
        'task_dep': ['tidy'],
        'actions': [
            'git clean -fd',
            'git reset --hard HEAD',
        ],
    }

if __name__ == '__main__':
    print('should be run with doit installed')
    import doit
    doit.run(globals())
