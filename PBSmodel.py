import logging
import os
class PBSMODEL ():
	path=r'D:\Diploma\testProg\THOR\Device\jobs.txt'
	def __init__(self):
		self.logger=logging.getLogger('THOR.thor.PBSMODEL')
	def suspend(self):
		os.remove(PBSMODEL.path)
		self.logger.info('Suspend job finished successfully.')
	def resume(self):
		f = open(PBSMODEL.path, 'a')
		f.write('Resume finished successfully.\n')
		f.close()
		self.logger.info('Resume job finished successfully.')
	def checkstate(self):
		self.logger.info('Checking jobs state')
		if os.path.exists(PBSMODEL.path):
			return True
		else:
			return False

