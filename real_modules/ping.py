import subprocess
import logging

class Ping ():
    _ping_cmd = 'ping -n 2 -w 3 %(ipaddr)s'

    def __init__(self,ipaddr):
        self.status = False
        self.pingcfg = {}
        self.pingcfg['ipaddr'] = ipaddr
        self.logger = logging.getLogger('THOR.Monitor.Ping')
    def monitor(self):
        cmd = self._ping_cmd % self.pingcfg
        self.logger.info('Checking %(ipaddr)s availability using ping', self.pingcfg)
        self.logger.debug('Invoking command: %s', cmd)
        try:
            output = subprocess.check_output(cmd,shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.info('Ping %(ipaddr)s failed. Node considered down', self.pingcfg)
            self.status = False
        else:
            self.logger.info('Ping %(ipaddr)s finished successfully.', self.pingcfg)
            self.status = True
    def getStatus(self):
        return self.status
