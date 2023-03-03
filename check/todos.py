import logging
from toolsmod.common import Common
import toolsmod
from toolsmod.text_box import Text_box
from toolsmod.text import Text
from toolsmod.lang import Lang

Lang.add('cz','getTodos_001','Hledam #TODO ve schematu... ')
Lang.add('cz','getTodos_002','NALEZENO')
Lang.add('cz','getTodos_003','Strana: %-6s %-s')

Lang.add('en','getTodos_001','Finding TODOS (#TODO) in diagram... ')
Lang.add('en','getTodos_002','FOUND')
Lang.add('en','getTodos_003','Page  : %-6s %-s')

def getTodos(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK = '\033[92m'

    print(Lang.get('getTodos_001'), end='')
    regex = '.*(# *TODO.*)'
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
        print(FAIL + Lang.get('getTodos_002') + ENDC)
    for ii, txt in todos:
        print(FAIL+Lang.get('getTodos_003') % (ii.getPosPage(), txt.replace('\\n', '\n               '))+ENDC)
    return False
