import re
import logging
class Common():
	#najde hodnotu dle daneho reg. vyrazu
	@classmethod
	def find(self, where, what):
		m = re.match(what, where)
		if m:
			return m.groups()
		return None
	#zmeni hodnoty dle regexu
	#nval tupple
	@classmethod
	def replace(self, where, what, nval):	
		m = re.match(what, where)
		if m and len(nval) == m.lastindex:
			st = 0;
			a = ''
			for ii in range(0, m.lastindex):
				a = a + where[st:m.start(ii+1)]+ str(nval[ii])
				st = m.end(ii+1)
			a = a + where[st:]	
			return a
		return None
	@classmethod	
	def calcPosH(self, val):
		v = val
		border = [0.0, 59.944, 109.982, 160.02, 210.058, 260.096, 32000.0]
		pos =    ['-', '1', '2', '3', '4', '5', '6']
		for ii in range(0, len(border)):
			if v <= border[ii]:
				return pos[ii]
		return None
	@classmethod	
	def calcPosV(self, val):
		v = val
		border = [0.0, 60.198, 110.236, 160.02,32000.0]
		pos =    ['-', 'A', 'B', 'C', 'D']
		for ii in range(0, len(border)):
			if v <= border[ii]:
				return pos[ii]
		return None
	@classmethod
	def readEmptyLines(self, raw , lines):
		while lines:
			line = lines.pop(0)
			if len(line.strip()) == 0:
				logging.debug('Common: nacten prazdny radek do komponenty')
				raw.append(line)
			else:
				lines.insert(0, line)
				logging.debug('Common: radek neni prazdny -> vraceno')
				return	

	
	
