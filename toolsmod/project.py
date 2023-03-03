from toolsmod.abstract import Abstract
import logging
class Project(Abstract):
    def __init__(self, parent, lines, nested):
        Abstract.__init__(self, parent, lines, nested)

        logging.debug('Project : read from file: %s'% self.raw)
    	
		
