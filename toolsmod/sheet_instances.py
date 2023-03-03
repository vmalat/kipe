from toolsmod.abstract import Abstract
import logging
class Sheet_instances(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Sheet_instances : read from file: %s'% self.raw)
    	
		
