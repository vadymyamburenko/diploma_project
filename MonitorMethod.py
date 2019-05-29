import logging
import os

class MONITORMETHOD ():
	path=r'D:\Diploma\testProg\THOR\Device\\'
	def __init__(self,node):
		self.status = False
		self.logger = logging.getLogger('THOR.thor.MONITORMETHOD')
		self.monitorcfg = {}
		self.monitorcfg['node'] = node
		self.monitorcfg['path'] = MONITORMETHOD.path+node+'.txt'
	def monitor(self):
		if os.path.exists(self.monitorcfg['path']):
			self.status=True
		else:
			self.status=False
		self.logger.info('MONITORING NODE ' + self.monitorcfg['node'])
	def getStatus(self):
		return self.status
