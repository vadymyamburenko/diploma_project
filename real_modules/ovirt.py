import logging
import time
import ovirtsdk4 as sdk
import ovirtsdk4.types as types

class OVIRT():
    def _init_(self)
        self.logger = logging.getLogger('THOR.PowerCTL.ovirt')
    def connect(self)    
        connection = sdk.Connection(url, username, password, ca_file)
        return connection.system_service().vms_service()
    def stop_vm(self, name, vms_service)
        vm = vms_service.list(search='name='+ name)[0]
        vm_service = vms_service.vm_service(vm.id)
        vm_service.stop()
        logger.info("VM '%s' turning off" % (name))
        connection.close()
    def start_vm(self, name, vms_service)
        vm = vms_service.list(search='name='+name)[0]
        vm_service = vms_service.vm_service(vm.id)
        vm_service.stop()
        logger.info("VM '%s' turning on" % (name))
        connection.close()