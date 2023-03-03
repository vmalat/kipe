from toolsmod.abstract import Abstract
from toolsmod.common import Common
import os
import logging
class Sheet(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)
        self.sheet = None
        logging.debug('Sheet : read from file: %s'% self.raw)
    	
    def parseFinished(self):
        ret = [self]
        self.getChilds(ret)	
        for ii in ret:
            ret = ii.getField('Sheetfile')
            #print('Pridavam: %s'%ret)
            if ret:
                
                a = os.path.dirname(self.parent.filename) + '/' +ret
                #print('cist list %s'%a)
                self.sheet = self.getRoot().parseSheet(a) #let Kicad_sch register in Kicad_pro.childs
                self.sheet.parent = self #rewrite Kicad_sch.parent
                return
    
    def delete(self):
        self.parent.childs.remove(self)
        self.getRoot().childs.remove(self.sheet)


    def getFilename(self):
        #ret = [self]
        #self.getChilds(ret)	
        #for ii in ret:
        #    r = ii.getField('Sheetfile')
        #    if r:
        #        return r
        return self.getField('Sheetfile')

    def getPageNum(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(page "(.*)"\).*$')
            if r:
                return int(r[0])
        return None

    def setPageNum(self, num):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._replace('^ {'+str(ii.nested)+'}\(.*\(page "(.*)"\).*$',(str(num),))
            if r:
                return r
        return None
    
    def getPosX(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(at ([-0-9]*\.[0-9]*) [-0-9]*\.?[0-9]*.*\).*$')
            if r:
                return float(r[0])
        return 0.0

    def getPosY(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(at [-0-9]*\.[0-9]* ([-0-9]*\.?[0-9]*).*\).*$')
            if r:
                return float(r[0])
        return 0.0
    
    def getReference(self):
        return self.getField('Sheetname')