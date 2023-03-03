from toolsmod.abstract import Abstract
from toolsmod.sheet_instances import Sheet_instances
import logging
class Symbol(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Symbol : read from file: %s'% self.raw)
    
    def getReference(self):
        ret = [self]
        self.getChilds(ret)	
        for ii in ret:
            r = ii.getField('Reference')
            if r:
                return r

    def setReference(self, val):
        ret = [self]
        self.getChilds(ret)	
        for ii in ret:
            r = ii.setField('Reference',val)
            if r:
                return r

    def getLibrary(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(symbol \(lib_id "(.*)"\) \(.*\).*$')
            #TODO
            #print('\nRes:',r[0],' :',ii.raw.rstrip(),'  :  ', '^ {'+str(ii.nested)+'}\(symbol \(lib_id "(.*)"\) \(.*\).*$')
            if r:
                return r[0]
        return None


    def getPosPage(self):
        node = self.parent.parent # symbol.parent = kicad_sch, kicad_sch.parent = (kicad_pro or sheet)
        if node.sheet is None:
            node = self.parent
            if node is not None:
                nodes = []
                node.getChildsClass(nodes, Sheet_instances)
                for ii in nodes:
                    instances = []
                    ii.getChilds(instances)
                    for jj in instances:
                        r = jj._find('^ {'+str(jj.nested)+'}\(.*\(page "(.*)"\).*$')
                        if r:
                            return int(r[0])
            return 0
        else:
            nodes = [node]
            node.getChilds(nodes)
            for ii in nodes:
                r = ii._find('^ {'+str(ii.nested)+'}\(.*\(page "(.*)"\).*$')
                if r:
                    return int(r[0])
        return 0
    		


