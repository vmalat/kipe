import logging
from toolsmod.lang import Lang

Lang.add('cz','chkDup_001','Kontrola duplicit symbolu... ')
Lang.add('cz','chkDup_002','Duplicitni symbol %s na strane %s')

Lang.add('en','chkDup_001','Checking symbols duplicity... ')
Lang.add('en','chkDup_002','Duplicite symbol %s on page %s')

def checkDuplicity(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'

    print(Lang.get('chkDup_001'), end='')
    logging.info('CheckDuplicity: Running...')
    comps = project.findCompRegex('.*')
    logging.info('CheckDuplicity: %d symbols found'%len(comps))
    toCheck = []
    for ii in comps:
        toCheck.append(ii.getReference())
    toCheck.sort()
    err = False
    for ii in range(1, len(toCheck)):
        if toCheck[ii - 1] == toCheck[ii]:
            if not err:
                print(FAIL +Lang.get('error')+ENDC)
            err = True
            #nalezeni kde:
            rep = project.findCompRegex(toCheck[ii])
            for ii in rep:
                print(FAIL + Lang.get('chkDup_002')  %(ii.getReference(), ii.getPositionHuman()) + ENDC)
    if not err:
        print(OK + Lang.get('ok') + ENDC)
    return err
