import logging
from toolsmod.row import Row
from toolsmod.title_block import Title_block
from toolsmod.lang import Lang

Lang.add('cz','mkTitleBlock_001','Kontroluji/nastavuji TitleBlock ve schematu... ')

Lang.add('en','mkTitleBlock_001','Checking / setting TitleBlock in diagram... ')


def mkTitleBlock(project, cmdline):
    INFO = '\033[36m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OK   = '\033[92m'
    err = False
    print(Lang.get('mkTitleBlock_001'), end='')
    logging.info('mkTitleBlock: Running... ')


    for ii in project.childs:      
        content = []
        content.append('  (title_block\n')
        content.append('    (title "${DOC_TITLE}")\n')
        content.append('    (date "${DOC_DATE}")\n')
        content.append('    (rev "${DOC_REV}")\n')
        content.append('    (comment 1 "${DOC_ID}")\n')
        content.append('    (comment 2 "${DOC_CHANGESET}")\n')
        content.append('    (comment 3 "${CREATED_BY}")\n')
        content.append('    (comment 4 "${CHECKED_BY}")\n')
        content.append('  )\n')
        content.append('\n')

        #TODO predelat na title_block
        title = Title_block(None, content, 0)  
        while(content):
            Row(title, content, 2)
        
        nodes = [title]
        title.getChilds(nodes)

        for ii in project.childs:
            ii.addTitleBlockRaw(title) 


    if not err:
        print(OK + Lang.get('ok') + ENDC)
    else:
        print(FAIL + Lang.get('error') + ENDC)
    return err
