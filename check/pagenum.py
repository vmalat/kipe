import logging
from toolsmod.sheet import Sheet
from toolsmod.lang import Lang

Lang.add('cz','getPagenum_001','Nastavuji se cisla stranek... ')

Lang.add('en','getPagenum_001','Setting numbers of pages... ')

def sortpos(comp):
    #return '%05d' % comp.getPosPage() +str(comp.getPosX)+str(comp.getPosY)
    aa=comp.getPosY()
    return aa

def sort(sheet, list):
    aa = []
    sheet.getChildsClass(aa, Sheet)
    aa.sort(key=sortpos)
    for ii in aa:
        list.append(ii)
        sort(ii.sheet, list)    


def setPageNum(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'
    err = False
    print(Lang.get('getPagenum_001'), end='')
    pagenum = 1
    sheets = []
    for ii in project.childs:
        sheets.append(ii)

    sh = sheets.pop(0)
    #prvni PSheet - nema componentu
    sh.setPageNum(pagenum)
    

   
    sorted = []
    sort(sh, sorted)
    for ii in sorted:
        pagenum = pagenum + 1
        ii.setPageNum(pagenum)

    if not err:
        print(OK + Lang.get('ok') + ENDC)
    else:
        print(FAIL + Lang.get('error') +ENDC)
    return err
