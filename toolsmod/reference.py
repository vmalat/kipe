from toolsmod.abstract import Abstract
import logging
class Reference(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Row : read from file: %s'% self.raw)
    	
		
