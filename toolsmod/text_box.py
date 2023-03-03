from toolsmod.abstract import Abstract
import logging
class Text_box(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Path : read from file: %s'% self.raw)
    	
    def getPosPage(self):
        node = self.parent.parent # symbol.parent = kicad_sch, kicad_sch.parent = (kicad_pro or sheet)
        if node.sheet is None:
            node = self.parent
            if node is not None:
                nodes = []
                node.getChilds(nodes)
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

    def getPosY(self):
        nodes = [self]
        self.getChilds(nodes)
        for ii in nodes:
            r = ii._find('^ {'+str(ii.nested)+'}\(at .* ([-0-9]*\.?[0-9]*) .*\) .*\(.*\).*$')
            if r:
                return float(r[0])
        return 0.0