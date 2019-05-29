import logging
import os

class POWERMETHOD ():
	path=r'D:\Diploma\testProg\THOR\Device'
	def __init__(self,node):
		self.powercfg = {}
		self.powercfg['node'] = node
		self.powercfg['path'] = os.path.join(POWERMETHOD.path,node+'.txt')
		self.logger = logging.getLogger('THOR.thor.POWERMETHOD')
	def poweroff(self):
		os.unlink(self.powercfg['path'])
		self.logger.info('Power down ' + self.powercfg['node']+ ' finished.')
	def poweron(self):
		f = open(self.powercfg['path'], 'a')
		f.write('Power on finished successfully. \n')
		f.close()
		self.logger.info('Power on ' +self.powercfg['node']+' finished.')