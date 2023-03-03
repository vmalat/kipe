import logging
from toolsmod.lang import Lang

Lang.add('cz','checkGlabels_001','Vytvarim odkazy pro globalni navesti... ')
Lang.add('cz','checkGlabels_002','Chybi navesti %s, posledni na strane %d')
Lang.add('cz','checkGlabels_003','Predchozi a nasledujici navesti %s jsou na stejne strane %d')

Lang.add('en','checkGlabels_001','Creating references for global labels... ')
Lang.add('en','checkGlabels_002','Global label %s missing, last is on page %d')
Lang.add('en','checkGlabels_003','Previous and next global labels %s are on same page %d')

def calcXYref(comp):
    offset = 2.54
    x = comp.getPosX()
    y = comp.getPosY()
    orient = comp.getOrientation()
    logging.debug('calcXYref: %s %s %s %s'%(comp.getLabel(),str(x),str(y),str(orient)))
    if orient == 0: #right
        y = y + offset
        #orient = 2
    elif orient == 90: #up
        x = x + offset
    elif orient == 180: #left
        y = y + offset
        orient = 0
    else:            #down
        x = x + offset
        orient = 90
    return x, y, orient

def sortpos(comp):
    #return '%05d' % comp.getPosPage() +str(comp.getPosX)+str(comp.getPosY)
	return '%05d%05d%05d'%(int(comp.getPosPage()),int(comp.getPosX()),int(comp.getPosY()))
def checkGlabels(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'

    print(Lang.get('checkGlabels_001'), end='')
    logging.info('CheckGlabels: Running...')
    #smazani puvodnich referenci
    #comps = project.findNoteRegex('^\/.*$')
    #logging.info('CheckGlabels: Nalezeno %d referenci ke smazani'%len(comps))
    #for ii in comps:
    #    project.delComp(ii)
    #nalezeni odkazu a doplneni refenreci
    comps = project.findGLabelRegex('.*')
    logging.info('CheckGlabels: %d reference found'%len(comps))
    toCheck = {}
    for ii in comps:
        lbl = ii.getLabel()
        if lbl not in toCheck.keys():
            toCheck[lbl]=[]
        toCheck[lbl].append(ii)
    err = False
    chkseq = []
    for ii in toCheck:
        lbl = toCheck[ii]
        lbl.sort(key=sortpos)
        if len(lbl) % 2 == 1: #musi byt sude
            if not err:
                print(FAIL + Lang.get('error') +ENDC)
            err = True
            print (FAIL + Lang.get('checkGlabels_002')% (lbl[0].getLabel(), lbl[-1].getPosPage())+ENDC)
        else:
            chkseq.append(lbl) #pridat pro check sequence
    for ii in chkseq:
        #print ''
        #print ii[0].getLabel()+':',
        #for jj in ii:
        #print str(jj.getPosPage())+',',
        for jj in range(1, len(ii), 2):
            #print('jj: %d'%jj)
            if ii[jj-1].getPosPage() == ii[jj].getPosPage():
                if not err:
                    print(FAIL + Lang.get('error') +ENDC)
                err = True
                print(FAIL+Lang.get('checkGlabels_003')%(ii[jj].getLabel(), ii[jj].getPosPage())+ENDC)
                for kk in ii:
                    print(sortpos(kk))
                break
            else:
                pass
                frst = ii[jj-1]
                sec = ii[jj]
                frst.setField('Intersheetrefs', '/'+sec.getPositionHuman())
                x, y, orient = calcXYref(frst)
                frst.setFieldPos('Intersheetrefs', str(round(x,2)), str(round(y,2)), str(orient))
                sec.setField('Intersheetrefs', '/'+frst.getPositionHuman())
                x, y, orient = calcXYref(sec)
                sec.setFieldPos('Intersheetrefs', str(round(x,2)), str(round(y,2)), str(orient))
                frst.setPropertyJustifyNone('Intersheetrefs')
                sec.setPropertyJustifyNone('Intersheetrefs')
                

    if not err:
        print(OK + Lang.get('ok') + ENDC)
    return err

