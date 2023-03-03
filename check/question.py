import logging
from toolsmod.common import Common
import toolsmod
from toolsmod.text_box import Text_box
from toolsmod.text import Text
from toolsmod.lang import Lang

Lang.add('cz','getQuestion_001','Hledam otevrene body ve schematu... ')
Lang.add('cz','getQuestion_002','NALEZENO')
Lang.add('cz','getQuestion_003','Strana: %-6s %-s')

Lang.add('en','getQuestion_001','Finding open point (#?) in diagram... ')
Lang.add('en','getQuestion_002','FOUND')
Lang.add('en','getQuestion_003','Page  : %-6s %-s')

def getQuestion(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK = '\033[92m'

    print(Lang.get('getQuestion_001'), end='')


    regex = '.*(# *\?.*)'
    todos = []
    comps = []
    project.getChildsClass(comps, Text)
    project.getChildsClass(comps, Text_box)
    
    for ii in comps:
        txt = ii.getLabel()
        if txt:
            r = Common.find(txt, regex)
            if r:
                todos.append((ii, r[0]))
    if len(todos) == 0:
        print(OK + Lang.get('ok') + ENDC)
    else:
        print(FAIL + Lang.get('getQuestion_002') + ENDC)
    for ii, txt in todos:
        print(FAIL+Lang.get('getQuestion_003') % (ii.getPosPage(), txt.replace('\\n', '\n               '))+ENDC)
    return False