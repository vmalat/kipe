from toolsmod.abstract import Abstract
import logging
class Instances(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Instances : read from file: %s'% self.raw)
    	
		
