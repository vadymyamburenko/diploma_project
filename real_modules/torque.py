import subprocess
import logging

class TORQUE ():
    torque_cmd = 'qstat -c'
    torque_cmd2= 'mjobctl -%(action)s -%(jobid)s'
    def __init__(self):
		self.torquecfg = { }
		self.logger = logging.getLogger('THOR.PowerCTL.TORQUE')
	def suspend(self):
		try:
			output = self.subprocess.check_output(torque_cmd, shell=True).decode('utf-8').strip
		except subprocess.CalledProcessError as e:
			self.logger.error('getting jobs information failed, error message is %s', e.output)
		else:
			self.logger.info('get jobs successfully')
		output = output.split('\n')
		self.torquecfg[action] = 's'
		for line in output[3:]:
			fields = line.split()
			if fields[4]=='R':
				self.torquecfg[jobid]=fields[0]
				cmd=self.torque_cmd2%self.torquecfg
				self.logger.info('Suspending job %(jobid)s', self.torquecfg)
				self.logger.debug('Invoking command: %s', cmd)
				try:
					result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
				except subprocess.CalledProcessError as e:
					self.logger.error('Suspend failed. Error message: %s', e.output)
				else:
					self.logger.info('Suspend job finished successfully. %s', output)
	def resume(self):
		try:
			output = self.subprocess.check_output(torque_cmd, shell=True).decode('utf-8').strip
		except subprocess.CalledProcessError as e:
			self.logger.error('getting jobs information failed, error message is %s', e.output)
		else:
			self.logger.info('get jobs successfully')
		output = output.split('\n')
		self.torquecfg[action] = 'r'
		for line in output[3:]:
			fields = line.split()
			if fields[4] == 'S':
				self.torquecfg[jobid] = fields[0]
				cmd = self.torque_cmd2 % self.torquecfg
				self.logger.info('Resuming job %(jobid)s', self.torquecfg)
				self.logger.debug('Invoking command: %s', cmd)
				try:
					result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
				except subprocess.CalledProcessError as e:
					self.logger.error('Resume failed. Error message: %s', e.output)
				else:
					self.logger.info('Resume job finished successfully. %s', output)
	def checkstate(self):
		try:
			output = self.subprocess.check_output(torque_cmd, shell=True).decode('utf-8').strip
		except subprocess.CalledProcessError as e:
			self.logger.error('getting jobs information failed, error message is %s', e.output)
		else:
			self.logger.info('get jobs successfully')
		jobon=False
		output = output.split('\n')
		for line in output[3:]:
			fields = line.split()
			if fields[4] == 'R':
				jobon=True
		self.logger.info('Cheking job state')
        return jobon
	
