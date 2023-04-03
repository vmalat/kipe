#Abstract class - base for all classes in toolsmod
from toolsmod.common import Common

import logging
class Abstract():
    def __init__(self, parent, lines, nested):
        self.parent = parent        #parent node - nodes which is hierarchicaly "above"
        self.childs = []            #children nodes - nodes which are hierarchicaly "under"
        self.raw = ''   			#source rows from the schematic file
        self.nested = nested        #indentation of the line
        self.sheet = None
        if parent is not None:
            parent.childs.append(self)
        if lines:    
            line = lines.pop(0)         #read line from file
            self.raw = line             #save to raw
    
    def parseFinished(self):
        return None


    def _find(self, regex):
        if self.raw:
            logging.debug(str(self.__class__.__qualname__)+': _find: in %s finding %s'%(self.raw.rstrip(),regex))
            ret = Common.find(self.raw, regex)
            if ret:
                return ret
        return None
    
    
    def _replace(self, regex, nval):
        if self.raw:
            ret = Common.replace(self.raw, regex, nval)
            if ret:
                self.raw = ret
                return True
        return False


    
    def getPositionHuman(self):
        page = self.getPosPage()
        x = self.getPosX()
        y = self.getPosY()
        logging.debug(str(self.__class__.__qualname__)+': PositonHuman get x: %f y:%f'%(x,y))
        return str(page) +'.' + str(Common.calcPosV(y)) + str(Common.calcPosH(x))

    
    #TODO predelat
    def __repr__(self):
        return str(self.raw)

    def getLabel(self):
        r = self._find('^ {'+str(self.nested)+'}\(.*\"(.*)\".*$')
        if r:
            return r[0]
    
    def setLabel(self, val):
        r = self._replace('^ {'+str(self.nested)+'}\(.*\"(.*)\".*$', (val,))
        return r

    def getField(self, num):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            regex = '^ {'+str(ii.nested)+'}\(property \"'+str(num)+'\" \"(.*)\" \(.*\).*$'
            logging.debug(str(self.__class__.__qualname__)+': getField: %s: %s'%(str(num),ii.raw.rstrip()))
            r = ii._find(regex)
            if r:
                return r[0]
        return None
    


    def setField(self, field, val):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._replace('^ {'+str(ii.nested)+'}\(property "'+field+'" "(.*)" \(.*\).*$', (val,))
            if r:
                return r
        return None
    
        

    def getPosX(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(at ([-0-9]*\.?[0-9]*) .* .*\).*$')
            if r:
                return float(r[0])
        return 0.0

    def getPosY(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(at .* ([-0-9]*\.?[0-9]*) .*\).*$')
            if r:
                return float(r[0])
        return 0.0
        



    def setFieldPos(self, field, x, y, rot):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._replace('^ {'+str(ii.nested)+'}\(property "'+str(field)+'" .*\(at ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*)\).*$', (x,y,rot,))
            if r:
                return r


    def getOrientation(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(.*\(at .* .* ([0-9]*)\).*$')
            if r:
                return int(r[0])
        return None
    
    def delete(self):
        self.parent.childs.remove(self)

    def _iterator(self, list, func, data):
        for ii in self.childs:
            func(list,ii, data)
            ii._iterator(list, func, data)
        return list  

    def _getChilds(self, list,ii,data):
        list.append(ii)


    def _getChildsClass(self, list,ii,data):
        if isinstance(ii, data[0]):
            list.append(ii)    

    def getChilds(self, list):
        self._iterator(list, self._getChilds, (None,))


    def getChildsClass(self, list, child_class):
        self._iterator(list, self._getChildsClass, (child_class,))

    def getRoots(self):
        ret = []
        ii = self.parent
        while ii:
            ret.append(ii)
            ii = ii.parent
        return ret

    def getRoot(self):
        ii = self.parent
        if ii is None:
            return self
        if ii is not None:
            return(ii.getRoot())
        
    def getRootSheet(self, parent_class):
        ii = self.parent
        if ii is None:
            return None
        if ii is not None:
            if ii.sheet is not None:
                return ii
            else:
                return(ii.getRootSheet())
        
    def getUuid(self):
        for ii in self.childs:
            #print('getUuid:',ii.__class__,ii.nested,ii.raw)
            r = ii._find('^ {'+str(ii.nested)+'}\(uuid (.*)\).*$')
            if r:
                return str(r[0])
        return None

    def getInstancePath(self):
        roots = self.getRoots()
        ret = ''
        #go throght sheets
        for ii in roots:
            if ii.sheet is not None:
                ret = '/' + ii.getUuid() + ret 
        ii = roots[len(roots)-2] #second from end is first kicad_sch
        ret = '/' + ii.getUuid() + ret


        return ret
