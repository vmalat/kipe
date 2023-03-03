import logging
import os
from toolsmod.common import Common
from toolsmod.sheet import Sheet
from toolsmod.instances import Instances
from toolsmod.project import Project
from toolsmod.path import Path
from toolsmod.symbol import Symbol
from toolsmod.reference import Reference
from toolsmod.lang import Lang


Lang.add('cz','mkFlat_001','Kontroluji se duplicitni listy ... ')
Lang.add('cz','mkFlat_002','Kontoluji instance symbolu v projektu ... ')
Lang.add('cz','mkFlat_003','Duplicitni list %s pravdepodobne instance listu ... VYMAZANO')
Lang.add('cz','mkFlat_004','Nenalezena instance pro symbol/stranku %s')
Lang.add('cz','mkFlat_005','Nalezeno vice instanci pro symbol/stranku %s')
Lang.add('cz','mkFlat_006','Nenalezen (project pro symbol/stranku %s')
Lang.add('cz','mkFlat_007','Nenalezena (path pro symbol/stranku %s')
Lang.add('cz','mkFlat_008','Provedla se uprava (instance pro symbol/stranku %s')
Lang.add('cz','mkFlat_009','Nenalezeno spravne uuid v (path pro symbol %s')


Lang.add('en','mkFlat_001','Checking sheet duplicity ... ')
Lang.add('en','mkFlat_002','Checking project instances ... ')
Lang.add('en','mkFlat_003','Duplicate sheet %s probably instance of sheet ... DELETED')
Lang.add('en','mkFlat_004','Symbol/sheet instance found for %s')
Lang.add('en','mkFlat_005','More instances found for symbol/sheet %s')
Lang.add('en','mkFlat_006','Project for instance of %s not found')
Lang.add('en','mkFlat_007','Path for instance %s not found')
Lang.add('en','mkFlat_008','Symbol/sheet instance of %s adapted')
Lang.add('en','mkFlat_009','Correct path UUID for %s not found')


def mkFlat(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK = '\033[92m'
    lang = 'en'
    print(Lang.get('mkFlat_001'), end='')
    sheets = []
    project.getChildsClass(sheets, Sheet)
    result = []
    result_fail = []
    search = []
    err = False
    instance = False

    for ii in sheets:
        aa = ii.getFilename()
        if aa in search:
            ii.delete()
            result.append(Lang.get('mkFlat_003')%(os.path.basename(aa)))
        else:
            search.append(aa)
    if result_fail:
        print(FAIL + 'CHYBA' + ENDC)
    elif result:
        print(WARN + 'POZOR' + ENDC)
    else:    
        print(OK + 'OK' + ENDC)

    for ii in result:
        print(WARN+ii+ENDC)
    for ii in result_fail:
        print(FAIL+ii+ENDC)

    result = []
    result_fail = []

    print(Lang.get('mkFlat_002'), end='')
    prj_name = Common.replace(project.filename, '.*(\..*$)', ('',))
    #print('\nProjekt: '+prj_name)
    

    nodes = []
    project.getChildsClass(nodes, Symbol)
    project.getChildsClass(nodes, Sheet)
    
    for ii in nodes:
        instance_path = ii.getInstancePath()

        instances = []
        ii.getChildsClass(instances,Instances)

        if not instances:
            result.append(Lang.get('mkFlat_004')%ii.getReference())
            break

        if len(instances) > 1:
            result_fail.append(Lang.get('mkFlat_005')%ii.getReference())
            err = True
            break
        

        projects = []
        instances[0].getChildsClass(projects,Project)

        if not projects:
            result_fail.append(Lang.get('mkFlat_006')%ii.getReference())
            error = True
            break

        #najdu path 
        paths = []
        remain_path = None
        ii.getChildsClass(paths,Path)

        if not paths:
            result_fail.append(Lang.get('mkFlat_007')%ii.getReference())
            error = True
            break
        
        if len(paths) > 1 or len(projects) > 1:
            result.append(Lang.get('mkFlat_008')%ii.getReference())
            

        for jj in paths:
            r = jj._find('.*\"('+instance_path+')\".*')
            if r:
                remain_path = jj
                #print('Zachovat:', ii.raw)
                break
            else:
                pass
                #print('Ke smazani:', ii.raw)
        #print('hash path:%s\n'%instance_path)

        if remain_path:
            remain_project = projects[0]
            #delete all projects from (instances
            for kk in projects:
                kk.delete()
            paths_todel = []
            #delete all (path from (project
            remain_project.getChildsClass(paths_todel, Path)
            for kk in paths_todel:
                kk.delete()
            
            instances[0].childs.insert(0,remain_project)
            remain_project.parent = instances[0]
            remain_project.childs.insert(0, remain_path)
            remain_path.parent = remain_project
            remain_project.setLabel(prj_name)
            
            #sync reference from instances to field "Reference"
            ref = []
            remain_path.getChildsClass(ref, Reference)
            if ref:
                for kk in ref:
                    sync = ref[0].getLabel() # yes, label
                    ii.setReference(sync) 
            
        else:
            #path is not in (instances
            result_fail.append(Lang.get('mkFlat_009')%ii.getReference())
            error = True
            break
    if result_fail:
        print(FAIL + 'CHYBA' + ENDC)
    elif result:
        print(WARN + 'POZOR' + ENDC)
    else:    
        print(OK + 'OK' + ENDC)
                
        
    # if result_fail:
    #     print(FAIL + 'CHYBA' + ENDC)
    # else:    
    #     print(OK + 'OK' + ENDC)
                
    for ii in result:
        print(WARN+ii+ENDC)
    for ii in result_fail:
        print(FAIL+ii+ENDC)
    if result_fail:
        # print(FAIL+'\nPOZOR:\nNutne akce:\n1. otevrit projekt v aplikaci Kicad\n'\
        #       '2. doplnit rucne chybejici cisla stranek\n3. ulozit v aplikaci Kicad\n'\
        #       '4. ukoncit aplikaci Kicad'\
        #       '\n\nAplikace byla prepnuta do konzole.\nProjekt lze ulozit prikazem save-force '\
        #       'nebo ukoncit prikazem exit.'+ENDC) 
        print(FAIL+'\nPOZOR:\nNutne akce:\n1. otevrit projekt v aplikaci Kicad\n'\
              '2. ulozit v aplikaci Kicad\n'\
              '3. ukoncit aplikaci Kicad'+ENDC) 
        cmdline.clear()
        #cmdline.append('console')
        return True        
    

    return err