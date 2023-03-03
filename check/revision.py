import logging
from toolsmod.lang import Lang

Lang.add('cz','setRevision_001','Nastavuji revizi schematu... ')

Lang.add('en','setRevision_001','Setting revision of diagram... ')

def setRevision(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK = '\033[92m'

    print(Lang.get('setRevision_001'), end='')
    rev = cmdline.pop(0)
    err = not project.setProperty('DOC_REV', rev)
    if err:
        print(FAIL + Lang.get('error') + ENDC)
    else:
        print(OK + Lang.get('ok') + ENDC)
    return err