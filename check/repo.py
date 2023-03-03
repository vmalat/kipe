import logging
import os
import re
from toolsmod.common import Common
from toolsmod.lang import Lang

Lang.add('cz','checkRepo_001','Kontroluji stav repozitáře... ')
Lang.add('cz','checkRepo_002','Repozitar neni cisty: %s')
Lang.add('cz','setChangeset_001','Aktualizuji identifikaci repozitare... ')

Lang.add('en','checkRepo_001','Checking repository status... ')
Lang.add('en','checkRepo_002','Uncommited changes in repository: %s')
Lang.add('en','setChangeset_001','Setting repository identification... ')

def getChangeset():
    hg = os.popen('hg identify')
    hgIdent = hg.read()
    hg.close()
    return hgIdent


def checkRepo(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'

    print(Lang.get('checkRepo_001'), end='')
    hgIdent = getChangeset()
    r = re.match('^.*\+.*$', hgIdent)
    if r:
        print(FAIL + Lang.get('error') + ENDC)
        print(FAIL + Lang.get('checkRepo_002')%hgIdent.strip() + ENDC)
        return True
    else:
        print(OK + Lang.get('ok') + ENDC)
        return False

def setChangeset(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK = '\033[92m'

    print(Lang.get('setChangeset_001'), end='')
    hgIdent = getChangeset()
    err = False
    m = Common.find(hgIdent, '^(\S*)\s*.*$')
    if m:
        err = not project.setProperty('DOC_CHANGESET', m[0])
    else:
        err = True
    if err:
        print(FAIL + Lang.get('error') + ENDC)
    else:
        print(OK + Lang.get('ok') + ENDC)
    return err
