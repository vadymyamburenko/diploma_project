import subprocess
import logging

class PN7320 ():
    _pn7320_cmd = 'fence_altusen_snmp --ip %(ipaddr)s --community %(community)s --action %(action)s --plug %(plug)s'

    def __init__(self,ipaddr):
        self.pn7320cfg = {}
        self.pn7320cfg['ipaddr'] = ipaddr
        self.logger = logging.getLogger('THOR.PowerCTL.PN7320')
    def setCredentials(self,plug,community):
        self.pn7320cfg['plug']  = plug
        self.pn7320cfg['community']  = community
    def poweroff(self):
        self.pn7320cfg['action']  = 'off'
        cmd = self._pn7320_cmd % self.pn7320cfg
        self.logger.info('Powering down plug %(plug)s on PN7320 switched PDU', self.pn7320cfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.logger.error('Power down failed. Error message: %s', e.output)
        else:
            self.logger.info('Power down finished successfully. %s', output)
    def poweron(self):
        self.pn7320cfg['action']  = 'on'
        cmd = self._pn7320_cmd % self.pn7320cfg
        self.logger.info('Powering up plug %(plug)s on PN7320 switched PDU', self.pn7320cfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.logger.error('Power on failed. Error message: %s', e.output)
        else:
            self.logger.info('Power on finished successfully. %s', output)