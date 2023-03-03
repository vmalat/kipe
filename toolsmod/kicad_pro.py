#obsluha projektu
#parser projektu
import os
import logging
from toolsmod.common import Common
from toolsmod.abstract import Abstract
from toolsmod.kicad_sch import Kicad_sch
from toolsmod.symbol import Symbol
from toolsmod.global_label import Global_label
import toolsmod

class Kicad_pro(Abstract):
    def __init__(self, filename):
        Abstract.__init__(self, None, None, 0)
        self.filename = os.path.basename(filename)
        self.basedir = os.path.dirname(filename)
    
        self.childs = []
        logging.debug('PProject: Projektovy adresar: %s' % self.basedir)
        logging.debug('PProject: Projektovy soubor: %s' % self.filename)
        
        logging.debug('PProject: Cteni souboru %s'%self.basedir + os.sep + self.filename)
        f = open(self.basedir + os.sep + self.filename, 'r', encoding = "utf-8")
        self.raw = f.readlines()
        Kicad_sch(self, self.basedir + os.sep + Common.replace(self.filename, '.*\.(.*$)', ('kicad_sch',)))
    
    def parseSheet(self, file):
        #print('Project:parsuji ')
        sch = Kicad_sch(self, file)
        return sch
        
    def makeFilename(self, filename):
        return self.basedir + os.sep + filename
    def getComps(self):
        ret = []
        for ii in self.sheets:
            for jj in ii.comps:
                ret.append(jj)
        return ret
    def delComp(self, node):
        try:
            self.childs.remove(node)
            logging.info('PProject: Odstranena komponenta: %s'% comp.__class__)
            return True
        except:
            logging.error('PProject: Chyba pri odstranovani komponenty: %s'% comp.__class__)
            return False

    def findCompRegex(self, regex):
        ret = []
        symbols = []
        for ii in self.childs:
            ii.getChildsClass(symbols, Symbol)
        for ii in symbols:
            ref = ii.getReference()
            reg = '('+regex+')'
            if ref and Common.find(ref, reg):
                ret.append(ii)
        return ret
    
    def findGLabelRegex(self, regex):
        ret = []
        symbols = []
        for ii in self.childs:
            ii.getChildsClass(symbols,Global_label)
        for ii in symbols:
            ref = ii.getLabel()
            reg = '('+regex+')'
            if ref and Common.find(ref, reg):
                ret.append(ii)
        return ret
        

    def findCompClass(self, cl):
        a = self.getComps()
        ret = []
        for ii in a:
            if isinstance(ii, cl):
                ret.append(ii)
        return ret
    def findSheetRegex(self, regex):
        a = self.getComps()
        ret = []
        for ii in a:
            if isinstance(ii, toolsmod.csheet.CSheet):
                ref = ii.getLabel()
                reg = '('+regex+')'
                if ref and Common.find(ref, reg):
                    ret.append(ii)
        return ret
    def findNoteRegex(self, regex):
        a = self.getComps()
        ret = []
        for ii in a:
            if isinstance(ii, toolsmod.cnote.CNote):
                ref = ii.getLabel()
                reg = '('+regex+')'
                if ref and Common.find(ref, reg):
                    ret.append(ii)
        return ret

    def setProperty(self, prop, val):
        for ii in self.raw:
            r = Common.replace(ii, '^ {4}"'+str(prop)+'": "(.*)".*$', (val,))
            if r is not None:
                self.raw[self.raw.index(ii)] = r
                return True
        return False
    def save(self):
        f = open(self.basedir + os.sep + self.filename, 'w', encoding='utf-8')
        for ii in self.raw:
            f.write(ii)
        f.close()

        for ii in self.childs:
            ii.save()
    def getSheets(self):
        ret = []
        for ii in self.childs:
            ret.append(ii)
        return ret