# -*- coding: utf-8 -*-
import logging
import sys
import traceback
from toolsmod.kicad_pro import Kicad_pro
from check.duplicity import *
from check.content import *
from check.glabels import *
from check.subcomps import *
from check.repo import *
from check.revision import *
from check.question import *
from check.todos import *
from check.bom import *
from check.titleblock import *
from check.pagenum import *
from check.mkflat import *

#texts definition for this module
Lang.add('cz','error','CHYBA')
Lang.add('cz','ok','OK')
Lang.add('cz','kipe_001','ERROR: Wrong operator for load command')
Lang.add('cz','kipe_002','Nacitam projekt... ')
Lang.add('cz','kipe_003','Ukladam projekt... ')
Lang.add('cz','kipe_004','Nelze ulozit kvuli predchozim chybam')
Lang.add('cz','kipe_005','Neni nacten zadny projekt')
Lang.add('cz','kipe_006','Neznamy prikaz')
Lang.add('cz','kipe_007','Ukoncuji')

Lang.add('en','error','ERROR')
Lang.add('en','ok','OK')
Lang.add('en','kipe_001','ERROR: Wrong operator for load command')
Lang.add('en','kipe_002','Loading project... ')
Lang.add('en','kipe_003','Saving project... ')
Lang.add('en','kipe_004','Unable to save due to prevoius errors')
Lang.add('en','kipe_005','No project loaded')
Lang.add('en','kipe_006','Unknown command')
Lang.add('en','kipe_007','Exitting')



project = None
saveprohibited = False

cmds = [['chkdup', checkDuplicity],
        ['mkcontent', getContent],
        ['mksubs', checkSubcomps],
        ['mkrefs', checkGlabels],
        ['chkrepo', checkRepo],
        ['mkrepoid', setChangeset],
        ['mkrev', setRevision],
        ['pquestion', getQuestion],
        ['ptodos', getTodos],
		['mkbom', getBom],
        ['mktitle', mkTitleBlock],
        ['mkpgnum', setPageNum],
        ['mkflat', mkFlat]
]

INFO = '\033[36m'
WARN = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
OK = '\033[92m'

def refsort(cmp):
    a, b, c = Common.find(cmp.getReference(), '^(\D*)(\d*)\.?(\d*).*$')
    #return a,float('%05d' % int('0'+b))
    return '%s%05d%05d'%(a,int('0'+b),int('0'+c))

def findcr(project, cmdline):
    reg = cmdline.pop(0)
    cmps = project.findCompRegex(reg)
    cmps.sort(key=refsort)
    for ii in cmps:
        print('%-10s %-8s %-20s'%(ii.getReference(), ii.getPositionHuman(), ii.getLibrary()))


cmds.append(['findcr', findcr])


def cmdLoad(proj, cmdline):
    global project, saveprohibited
    if len(cmdline) <= 0:
        logging.error('Wrong operator for load command')
        print(Lang.get('kipe_001'))
        saveprohibited = True
    cmd = cmdline.pop(0)
    try:
        print(Lang.get('kipe_002'), end='')
        project = Kicad_pro(cmd)
        print(OK + Lang.get('ok') + ENDC)
        saveprohibited = False
    except Exception as e:        
        print(FAIL + Lang.get('error') + ENDC)
        logging.error(traceback.print_exc())
        saveprohibited = True


cmds.append(['load', None]) #formalne kvuli helpu, prikaz zpracovavan odlisnym zpusobem

def cmdSave(project, cmdline):
    if checkLoad(project):
        print(Lang.get('kipe_003'), end='')
        if saveprohibited:
            print(FAIL + Lang.get('error') + ENDC)
            print(FAIL + Lang.get('kipe_004') + ENDC)
            return True
        else:
            project.save()
            print(OK + Lang.get('ok') + ENDC)
            return False


cmds.append(['save', cmdSave])

def cmdSaveForce(project, cmdline):
    if checkLoad(project):
        print(Lang.get('kipe_003'), end='')

        project.save()
        print(OK + Lang.get('ok') + ENDC)
        return False


cmds.append(['save-force', cmdSaveForce])

def checkLoad(project):
    if not project:
        print(Lang.get('kipe_005'))
        return False
    return True


def cmdHelp(project, cmdline):
    for ii in cmds:
        print(ii[0])
    return False


cmds.append(['help', None]) #formal because of help command, command is evaluated by differn approach
cmds.append(['exit', None]) #formal because of help command, command is evaluated by differn approach
cmds.append(['console', None]) #formal because of help command, command is evaluated by differn approach
cmds.append(['lang-en', None]) #formal because of help command, command is evaluated by differn approach
cmds.append(['lang-cz', None]) #formal because of help command, command is evaluated by differn approach

logging.basicConfig(filename='kipe.log',filemode='w',level=logging.CRITICAL)

#a = Kigtproject('ss1.sch')
if __name__ == "__main__":
    fromcmdline = False
    args = sys.argv
    args.pop(0)
    if len(args) > 0:
        fromcmdline = True
    #	print(args)
    while True:
        if fromcmdline:
            cmdline = args
            if len(args) == 0:
                exit(0)
        else:
            line = input('>>>')
            cmdline = line.split()
        while len(cmdline) > 0:
            cmd = cmdline.pop(0)
            if cmd == 'exit':
                print(Lang.get('kipe_007'))
                exit(0)
            elif cmd == 'load':
                cmdLoad(project, cmdline)
            elif cmd == 'help':
                cmdHelp(project, cmdline)
            elif cmd == 'console':
                fromcmdline = False
            elif cmd == 'lang-cz':
                Lang.setLang('cz')
            elif cmd == 'lang-en':
                Lang.setLang('en')
            else:
                ok = 0
                for ii in cmds:
                    if ii[0] == cmd:
                        if checkLoad(project):
                            if ii[1](project, cmdline):
                                saveprohibited = True
                            ok = 1
                        else:
                            ok = 1
                        break
                if ok == 0:
                    print(Lang.get('kipe_006'))

