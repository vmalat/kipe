from toolsmod.abstract import Abstract
import logging
class Path(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Path : read from file: %s'% self.raw)
    	
		
