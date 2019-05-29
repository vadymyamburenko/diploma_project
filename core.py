from thor import PBSmodel
from thor import PowerMethod
from thor import MonitorMethod
import configparser
import logging
import time
import core
class Core():
	def __init__(self):
		self.logger=logging.getLogger('THOR.Core')
	def transition(self, event):
		k=core.Core()
		state = k.checkstate()
		prevStateRes = 'state/' + state + '/resourses'
		stateperehod = 'state/' + state + '/transition'
		config_n=configparser.ConfigParser()
		config_n.read(r'D:\Diploma\testProg\THOR\configTest.ini')
		if config_n.has_option(stateperehod,event):
			staten=config_n.get(stateperehod,event)
			self.logger.info("Transition from " + state + " to " + staten)
			nextStateRes = 'state/' + staten + '/resourses'
			for res in config_n.options(nextStateRes): #for each resourse in state 
				if config_n.get(prevStateRes, res) != config_n.get(nextStateRes, res):  # if resourse state mismatch
					resourse= 'group/'+ res
					if config_n.has_option(resourse, 'power_method'):       #if power_method option in group section
						if config_n.get(resourse, 'power_method')=='PBSmodel':    #section for PBSMODEL
							powerchange=PBSmodel.PBSMODEL()
							if config_n.get(prevStateRes, res)=='on':         #if it was turned on
								powerchange.suspend()
							else:
								powerchange.resume()
					else:
						members = config_n.get(resourse, 'members').split(",")     #if powermetod in node
						for node in members:
							nodeSection="node/"+node
							if config_n.get(nodeSection, 'power_method')=='PowerMethod':    #section for power_method
								powerchange=PowerMethod.POWERMETHOD(config_n.get(nodeSection,'id'))
							if config_n.get(prevStateRes, res)=='on':         #if it was turned on
								powerchange.poweroff()
							else:
								powerchange.poweron()
			time.sleep(2)
			ch=core.Core()
			stateafter=ch.checkstate()
			if stateafter!=staten:
				self.logger.error(stateafter + ' +++++++++++++++++ ' + staten)
				ch.transition(event)
	def checkstate(self):
		config_n=configparser.ConfigParser()
		curentstate={}
		config_n.read(r'D:\Diploma\testProg\THOR\configTest.ini')
		config_resourses = [ s for s in config_n.sections() if s.startswith('group/') ]
		for s in config_resourses:
			if config_n.has_option(s, 'monitor_method'):       #if power_method option in group section
				if config_n.get(s, 'monitor_method')=='PBSmodel':    #section for PBSMODEL
					powerchange=PBSmodel.PBSMODEL()
					if powerchange.checkstate():
						curentstate[s[6:]]="on"
					else:
						curentstate[s[6:]]="off"
			else:
				members = config_n.get(s, 'members').split(",")     #if powermetod in node
				memberscount=len(members)
				groupstatus=0
				for node in members:
					nodeSection="node/"+node
					if config_n.get(nodeSection, 'monitor_method')=='MonitorMethod':    #section for monitoring node
						monitortool=MonitorMethod.MONITORMETHOD(config_n.get(nodeSection, 'id'))
						monitortool.monitor()
						if monitortool.getStatus():
							groupstatus+=1
				if groupstatus>=memberscount/2:
					curentstate[s[6:]]="on"
				else:
					curentstate[s[6:]]="off"		
		config_states = [ s for s in config_n.sections() if s.endswith('/resourses') ]
		for s in config_states:
			if config_n.get(s,'jobs')==curentstate['jobs'] and config_n.get(s,'wns')==curentstate['wns'] and config_n.get(s,'storage')==curentstate['storage']:
				s=s[6:-10]
				return s