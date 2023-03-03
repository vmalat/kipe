import logging
from toolsmod.symbol import Symbol
from toolsmod.kicad_sch import Kicad_sch
from toolsmod.lang import Lang

Lang.add('cz','getBom_001','Vytvarim BOM... ')

Lang.add('en','getBom_001','Creating BOM... ')

def getBom(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'
    err = False
    print(Lang.get('getBom_001'), end='')
    logging.info('getBom: creating BOM... ')
    comps = []
    project.getChildsClass(comps, Symbol)
    logging.info('MakeBOM: %d symbols found'%len(comps))
    result = []
    for ii in comps:
        if not isinstance(ii.parent, Kicad_sch):
            continue
        #print(ii.__class__)
        ref = ii.getReference()
        vendor = ii.getField('VENDOR')
        vendorid = ii.getField('VENDORID')
        crosssection = ii.getField('CROSSSECTION')
        #print(ref, vendor)
        if (ref is not None) or (vendor is not None) or (vendorid is not None) or (crosssection is not None): 
            result.append("%8s %8s %20s %40s %20s"%(ref, ii.getPositionHuman() ,vendor, vendorid, crosssection)) #

    if not err:
        print(OK + Lang.get('ok') + ENDC)
    else:
        print(FAIL + Lang.get('error') + ENDC)
    for ii in result:
        print(ii)
    return err
