import logging

from toolsmod.common import Common
from toolsmod.abstract import Abstract
from toolsmod.row import Row
from toolsmod.global_label import Global_label
from toolsmod.sheet import Sheet
from toolsmod.instances import Instances
from toolsmod.project import Project
from toolsmod.path import Path
from toolsmod.symbol import Symbol
from toolsmod.sheet_instances import Sheet_instances
from toolsmod.property import Property
from toolsmod.title_block import Title_block
from toolsmod.lib_symbols import Lib_symbols
from toolsmod.text_box import Text_box
from toolsmod.text import Text
from toolsmod.reference import Reference

class Kicad_sch(Abstract):
    def __init__(self, parent, filename):
        Abstract.__init__(self, parent, None, 0)
        self.filename = filename
        #self.project = project
        #read source file
        logging.debug('PSheet: Cteni souboru %s'%self.filename)
        f = open(self.filename, 'r', encoding = "utf-8")
        lines = f.readlines()
        f.close()
 
        err = False
        self.parseNodes(self, lines,0)

        #ret = []
        #self.getChilds(ret)
        #for ii in ret:
        #    print('%02d %s'%(ii.nested, ii.raw.rstrip()))

        if err:
            raise Exception('Chyba behem cteni/parsovani souboru %s' % self.filename)
        logging.info('PScheet: Dokonceno nacteni souboru %s'%self.filename)
    def getFilename(self):
        return self.filename
    def getRevision(self):
        for ii in self.raw:
            m = Common.find(ii, 'Rev \"(.*)\".*')
            if m:
                return m[0]
        return None

    def setRevision(self, rev):
        for ii in self.raw:
            m = Common.replace(ii, 'Rev \"(.*)\".*', (rev,))
            if m:
                self.raw[self.raw.index(ii)] = m
                logging.debug('PScheet: Revision set:%s' % (m.strip()))
                return True
        return False
    def setChangeset(self, chset):
        for ii in self.raw:
            m = Common.replace(ii, 'Comment2 \"(.*)\".*', (chset,))
            if m:
                self.raw[self.raw.index(ii)] = m
                logging.debug('PScheet: Changeset set:%s' % (m.strip()))
                return True
        return False


    def save(self):
        #print('ukladam... %s'%self.filename)
        f = open(self.filename, 'w', encoding='utf-8')
        nodes = []
        self.getChilds(nodes)
        for ii in nodes:
            f.write(ii.raw)
        f.close()


    #TODO predelat    
    def findSheets(self):
        a = self.comps
        ret = []
        for ii in a:
            if isinstance(ii, toolsmod.csheet.CSheet):
                ret.append(ii)
        return ret
    def addComp(self, comp):
        self.comps.insert(len(self.comps), comp)

    

    def addTitleBlockRaw(self, content):
        for ii in self.childs:
            if ii.__class__ == Title_block:
                content.parent = ii.parent
                self.childs[self.childs.index(ii)] = content
                return True
            if ii.__class__ == Lib_symbols:
                content.parent = self
                self.childs.insert(self.childs.index(ii), content)
                return
        return False 
            

                

    def setPageNum(self, num):
        nodes = []
        self.getChildsClass(nodes, Sheet_instances)
        for ii in nodes:
            instances = []
            ii.getChilds(instances)
            for jj in instances:
                r = jj._replace('^ {'+str(jj.nested)+'}\(.*\(page "(.*)"\).*$',(str(num),))
                if r:
                    return r
        return None


    def getPageNum(self):
        if self.rootcomp is None: #bude mit sheet instance
            for ii in self.comps:
                if isinstance(ii,CSheetinstances):
                    return(ii.getPageNum())    
        else:
            return self.sheet.rootcomp.getPageNum()

        return False

    def parseNodes(self, parent, plines, pnested):	
        node = None
        while(plines):
            line = plines[0]
            type = Common.find(line, '^( *)([\()\S]*) ?.*$')
            nested = len(type[0])
            row = type[1]     
            
            if row == '':
                Row(parent, plines, pnested)
            elif nested == pnested: #header or footer
                if not self.childs: 
                    node = Row(parent, plines, nested)
                    #print('pridan header')
                elif row == ')':#footer
                    node = Row(parent, plines, nested)
                else:    
                    break #header
            elif nested < pnested:
                return
            else:
                #new node and parse new node
                if   row == '(global_label':
                    node =  Global_label(parent, plines, nested) 
                elif row == '(sheet':
                    node =  Sheet(parent, plines, nested) 
                elif row == '(symbol' and nested == 2:
                    node =  Symbol(parent, plines, nested)
                elif row == '(instances':
                    node =  Instances(parent, plines, nested)
                elif row == '(project':
                    node =  Project(parent, plines, nested)
                elif row == '(path':
                    node =  Path(parent, plines, nested)  
                elif row == '(sheet_instances':
                    node =  Sheet_instances(parent, plines, nested) 
                elif row == '(property':
                    node =  Property(parent, plines, nested) 
                elif row == '(title_block':
                    node =  Title_block(parent, plines, nested) 
                elif row == '(lib_symbols':
                    node =  Lib_symbols(parent, plines, nested) 
                elif row == '(text_box':
                    node =  Text_box(parent, plines, nested) 
                elif row == '(text':
                    node =  Text(parent, plines, nested) 
                elif row == '(reference':
                    node =  Reference(parent, plines, nested) 
                else:
                    node =  Row(parent, plines, nested) 
                ret = self.parseNodes(node, plines, nested)
                node.parseFinished()
        return node

    #def printstruct(self,comps,indent):
    #    for ii in comps:
    #        fmt = '%'+str(indent)+'s %s'
    #        print(fmt%('',ii))
    #        self.printstruct(ii.comps,indent+2)


			
