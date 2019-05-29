from thor import PowerMethod
from thor import MonitorMethod
from thor import PBSmodel
import configparser
import logging
import argparse
import core
import os

logger = logging.getLogger('THOR')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(r'D:\Diploma\testProg\THOR\logging.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.info("start log")

config_n=configparser.ConfigParser()
config_n.read(r'D:\Diploma\testProg\THOR\configTest.ini')
while True:
	trap=os.listdir('Trap')
	if trap:
		proctrap='event/'+trap[0]
		proctrap=proctrap[:-4]
		path=r'D:\Diploma\testProg\THOR\Trap\\'+trap[0]
		if config_n.has_section(proctrap):
			trans=core.Core()
			event=trap[0][:-4]
			logger.info("Registered " + event + " event" )
			trans.transition(event)
		os.remove(path)
		trap.pop(0)