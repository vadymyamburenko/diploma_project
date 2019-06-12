import subprocess
import logging

class IPMI ():
    _ipmitool = 'ipmitool -H %(ipaddr)s -U %(user)s -P %(password)s -I lanplus power %(action)s'

    def __init__(self,ipaddr):
        self.ipmicfg = {}
        self.ipmicfg['ipaddr'] = ipaddr
        self.logger = logging.getLogger('THOR.PowerCTL.IPMI')
    def setCredentials(self,user,password):
        self.ipmicfg['user']  = user
        self.ipmicfg['password']  = password
    def poweroff(self):
        self.ipmicfg['action']  = 'off'
        cmd = self._ipmitool % self.ipmicfg
        self.logger.info('Powering down node %(ipaddr)s using IPMI', self.ipmicfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.logger.error('Power down failed. Error message: %s', e.output)
        else:
            self.logger.info('Power down finished successfully. ' + output)
    def poweron(self):
        self.ipmicfg['action']  = 'on'
        cmd = self._ipmitool % self.ipmicfg
        self.logger.info('Powering on node %(ipaddr)s using IPMI', self.ipmicfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.logger.error('Power on failed. Error message: %s', e.output)
        else:
            self.logger.info('Power on finished successfully. %s', output)