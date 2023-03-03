import logging
import re
from toolsmod.common import Common
from toolsmod.symbol import Symbol
from toolsmod.lang import Lang

Lang.add('cz','chkSubcomps_001','Kontroluji a vytvarim odkazy na subkomponenty... ')
Lang.add('cz','chkSubcomps_002','Nepovoleny index subkomponenty %s.%d')
Lang.add('cz','chkSubcomps_003','Nelze precist pole %s komponenty %s')
Lang.add('cz','chkSubcomps_004','Nenalezena povinna komponenta %s.%d')
Lang.add('cz','chkSubcomps_005','Nelze nastavit pole REF%d u komponenty %s ')
Lang.add('cz','chkSubcomps_006','Nevyuzita komponenta %s.%d')
Lang.add('cz','chkSubcomps_007','Nepovolena subkomponenta %s pro %s.%d %s')
Lang.add('cz','chkSubcomps_008','Nelze nastavit pole REF%d u komponenty %s')
Lang.add('cz','chkSubcomps_009','Nelze nastavit pole REF1 u subkomponenty %s.%d')
Lang.add('cz','chkSubcomps_010','Nelze nastavit pole PIN%d u subkomponenty %s.%d ')
Lang.add('cz','chkSubcomps_011','Nenalezena nosna komponenta pro subkomponentu %s /%s')

Lang.add('en','chkSubcomps_001','Checking and creating references to subsymbols... ')
Lang.add('en','chkSubcomps_002','Unallowed index of subsymbol %s.%d')
Lang.add('en','chkSubcomps_003','Can\'t read filed  %s of symbol %s')
Lang.add('en','chkSubcomps_004','Mandatory symbol %s.%d not found')
Lang.add('en','chkSubcomps_005','Can\'t set field REF%d in subsymbol %s ')
Lang.add('en','chkSubcomps_006','Unused symbol %s.%d')
Lang.add('en','chkSubcomps_007','Unallowed subsymbol %s for %s.%d %s')
Lang.add('en','chkSubcomps_008','Can\'t set field REF%d for symbol %s')
Lang.add('en','chkSubcomps_009','Can\'t set field REF1 for subsymbol %s.%d')
Lang.add('en','chkSubcomps_010','Can\'t set field PIN%d for subsymbol %s.%d ')
Lang.add('en','chkSubcomps_011','Root symbol for subsymbol %s /%s not found')



def checkSubcomps(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'
    print(Lang.get('chkSubcomps_001'), end='')
    warning = []
    logging.info('CheckSubcomps: Running...')
    comps = project.findCompRegex('^\s*[^\.]*\s*$')

    logging.info('CheckSubcomps: %d symbols found'%len(comps))
    #toCheck = []
    #for ii in comps:
    #	toCheck.append(ii.getReference())
    #toCheck.sort()
    err = False

    #vymazani REF1 poli u komponent
    subcomp_to_check = project.findCompRegex('^.*\..*$')
    logging.info('CheckSubcomps: %d subcomponents found'%len(subcomp_to_check))   
    for ii in subcomp_to_check:
        #vymaze referenci
        ret0 = ii.setField('REF1', '~')    
 
    subcomps = 0    
    for ii in comps:
        maincomlib = Common.find(ii.getLibrary(), '^(.*:).*$')
        if maincomlib is None:
            maincomlib = ''
        else:
            maincomlib = maincomlib[0]		
        comp = ii.getReference()
        for jj in range(1, 1000): #pouze 998 subkomponent
            subs = 'SUB'+str(jj)
            subfield = ii.getField(subs)
            if not subfield:
                subcomps = jj - 1
                logging.debug('CheckSubcomps: %d subcomponents for %s found' % (subcomps, comp))
                #kontrola zda neexistuji subkomponenty s vyssim subindexem nez povoluje base komponenta
                ccheck = project.findCompRegex('^\s*'+comp+'\.\d*\s*$')
                for kk in ccheck:
                    r = re.match('^\s*\S*\.(\d*)\s*$',kk.getReference())
                    if r:
                        actsub = int(r.group(1))
                        if ii.getLibrary() != '_material': #_material se nekontroluje na subkomponenty
                            if actsub > subcomps:
                                if not err:
                                    print(FAIL +'CHYBA'+ENDC)
                                err = True
                                print(FAIL + Lang.get('chkSubcomps_002')%(comp, actsub) +ENDC)
                                break
                break
            else:
                m = re.match('^\s*(\S*)\s*;\s*(\S*)\s*;\s*(\S*)\s*$', subfield)
                if not m:
                    if not err:
                        print(FAIL +Lang.get('error')+ENDC)
                    err = True
                    print(FAIL + Lang.get('chkSubcomps_003')%(subs, comp) +ENDC)
                    logging.debug('CheckSubcomps: Field %s of component %s: %s unloadable'%(subs, comp, subfield))

                    err = True
                subopt, sublib, subpar = m.groups()
                subcomp = project.findCompRegex('^\s*'+comp+'\.'+str(jj)+'*\s*$')
                if not subcomp:
                    if subopt != 'O':
                        if not err:
                            print(FAIL +Lang.get('error')+ENDC)
                        err = True
                        print(FAIL + Lang.get('chkSubcomps_004')%(comp, jj) +ENDC)
                    ret0 = ii.setField('REF'+str(jj), '~') #pole REFx nesmi byt prazdne, kicad 4.0.7 ho smaze a dale nemuze skript spravne fungovat
                    if ret0 == False:
                        if not err:
                            print(FAIL + Lang.get('error') +ENDC)
                        err = True
                        print(FAIL + Lang.get('chkSubcomps_005')%(jj, comp) +ENDC)
                    warning.append(Lang.get('chkSubcomps_006')%(comp,jj))
                else:
                    #napl data subkomponenty
                    sublib = '^.*:'+sublib+'$'
                    r = Common.find(subcomp[0].getLibrary(), sublib)
                    #print(r)
                    if r is None: 
                        if not err:
                            print(FAIL +Lang.get('error')+ENDC)
                        err = True
                        #print(subcomp[0].__class__)
                        #a = [subcomp[0]]
                        #subcomp[0].getChilds(a)
                        #for zz in a:
                        #    print(zz.raw)    
                        print(FAIL + Lang.get('chkSubcomps_007')%(subcomp[0].getLibrary(),comp, jj, sublib) +ENDC)
                        continue
                    pars = subpar.split(',')
                    ret0 = ii.setField('REF'+str(jj), '/'+subcomp[0].getPositionHuman())
                    if ret0 == False:
                        if not err:
                            print(FAIL +Lang.get('error')+ENDC)
                        err = True
                        print(FAIL + Lang.get('chkSubcomps_008')%(jj, comp) +ENDC)
                    ret0 = subcomp[0].setField('REF1', '/'+ii.getPositionHuman())
                    if ret0 == False:
                        if not err:
                            print(FAIL +Lang.get('error')+ENDC)
                        err = True
                        print(FAIL + Lang.get('chkSubcomps_009')%(comp, jj) +ENDC)
                    pin = 1
                    for kk in pars:
                        pinval = kk.strip()
                        if pinval == '':
                            pinval = '~'
                        ret0 = subcomp[0].setField('PIN'+str(pin), pinval)
                        if ret0 == False:
                            if not err:
                                print(FAIL +Lang.get('error')+ENDC)
                            err = True
                            print(FAIL + Lang.get('chkSubcomps_010')%(pin, comp, jj) +ENDC)
                        pin = pin + 1
    #kontrola napolneni REF1 u subkomponent
    logging.info('CheckSubcomps: Checking of subcomponents withou the root component')                       
    for ii in subcomp_to_check:
        ret0 = ii.getField('REF1') 
        if ret0 == '~':
            if not err:
                print(FAIL +Lang.get('error')+ENDC)
            err = True
            print(FAIL + Lang.get('chkSubcomps_011')%(ii.getReference(), ii.getPositionHuman()) +ENDC)
        

    if not err:
        print(OK + Lang.get('ok') + ENDC)
    for ii in warning:
        print(WARN+ii+ENDC)
    return err
