from toolsmod.abstract import Abstract
import logging
class Property(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Instances : read from file: %s'% self.raw)

    def getLabel(self):
        r = self._find('^ {'+str(self.nested)+'}\(.*\"(.*)\" \".*\".*$')
        return r[0]
    	
		
