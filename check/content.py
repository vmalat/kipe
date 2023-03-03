import logging
import toolsmod
from toolsmod.sheet import Sheet
from toolsmod.text_box import Text_box
from toolsmod.lang import Lang

Lang.add('cz','getContent_001','Vytvarim obsah ... ')

Lang.add('en','getContent_001','Creating TOC ... ')


def sortPage(comp):
    return comp.getPageNum()

def getContent(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'

    num = 33 # polozek na textbox

    page = 1
    print(Lang.get('getContent_001'), end='')
    
    content = []
    project.getChildsClass(content, Sheet)
    content.sort(key=sortPage)

    
    out = []
    for ii in content:
        out.append('%-2d... %s'%(int(ii.getPageNum()), ii.getField('Sheetname')))
    
    
    print(OK +Lang.get('ok')+ENDC)

    #for ii in out:
    #    print(ii)
    #out = []
    #for ii in range(1,100):
    #    out.append('%-2d... aaa'%ii)
    sheet = project.childs[0]
    index = 0
    boxes = []
    project.childs[0].getChildsClass(boxes, Text_box) #only first page
    for ii in boxes:
        if ii.getPosY() > 40.0:
            txt = ''
            for jj in range(num):
                if not out:
                    break
                txt = txt+ out.pop(0)+'\n'
            ii.setLabel(txt.replace('\n','\\n'))


        
