import subprocess
import logging

class SNMPGet ():
    _snmpget_cmd = 'snmpget -v 2c -Oqve -c %(community)s %(ipaddr)s %(mib)s'

    def __init__(self,ipaddr):
        self.status = False
        self.snmpcfg = {}
        self.snmpcfg['ipaddr'] = ipaddr
        self.logger = logging.getLogger('THOR.Monitor.SNMPGet')
    def setCredentials(self,mib,community='public',expected_value='1'):
        self.snmpcfg['community'] = community
        self.snmpcfg['mib'] = mib
        self.snmpcfg['expected_value'] = expected_value
    def monitor(self):
        cmd = self._snmpget_cmd % self.snmpcfg
        self.logger.info('Checking node availability using SNMP MIB %(mib)s value from %(ipaddr)s', self.snmpcfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            self.logger.error('SNMP get from %(ipaddr)s failed. Node considered down. Error message: \n' + e.output, self.snmpcfg)
            self.status = False
        else:
            self.logger.info('SNMP get from %(ipaddr)s returned %(mib)s = ' + output + ' (expected: %(expected_value)s)', self.snmpcfg)
            if output == self.snmpcfg['expected_value']:
                self.status = True
            else:
                self.status = False
    def getStatus(self):
        return self.status