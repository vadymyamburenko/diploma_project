#!/usr/bin/python

import sys
import argparse
import logging
import ConfigParser

# parse command line arguments first
parser = argparse.ArgumentParser(description='Traps Handlers for Operation Recovery (THOR) traps parser for snmptrapd.')
parser.add_argument('-c', '--config', type=file, default='/root/powerconfig.ini', help='path to THOR configuration file. Default is /etc/thor.conf') #TODO: change real default
parser.add_argument('-d', '--debug', action='store_true', help='enables DEBUG logging to stderr')
parser.add_argument('--loglevel', choices=['DEBUG','INFO','ERROR','CRITICAL'], default='ERROR', help='configures logging level to stderr. Default is ERROR.')
cmd_args = parser.parse_args()

# defult values for configuration file
config_default = { 'logfile' : '/tmp/trapparser.log',
                   'loglevel': 'DEBUG',
                   'spooldir':  '/tmp/thor/traps' }

# initialize logger
logger = logging.getLogger('THOR.SNMPTrapParser')
logger.setLevel(logging.DEBUG)
# initialize stderr stream logging first
log_handler_stderr = logging.StreamHandler()
log_handler_stderr.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
# configure logging level
if cmd_args.debug:
    log_handler_stderr.setLevel(logging.DEBUG)
else:
    log_handler_stderr.setLevel(cmd_args.loglevel)

logger.addHandler(log_handler_stderr)

# read and parse THOR configuration file
try:
    config_p = ConfigParser.ConfigParser(config_default)
    config_p.read(cmd_args.config)
except IOError:
    logger.critical('Filed to open configuration file %s', cmd_args.config)
    sys.exit(1)

log_settings = {}
if config_p.has_section('log/TrapParser'):
    logger.debug('Getting logging settings from config [log/TrapParser] section')
    log_settings['logfile'] = config_p.get('log/TrapParser','logfile')
    log_settings['loglevel'] = config_p.get('log/TrapParser','loglevel')
else:
    logger.debug('Using configuration defaults for logging to file')
    log_settings = config_default


logger.debug('Initializing logging to file: %s on %s level', log_settings['logfile'], log_settings['loglevel'])
log_handler_file = logging.FileHandler(log_settings['logfile'])
log_handler_file.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log_handler_file.setLevel(log_settings['loglevel'])
logger.addHandler(log_handler_file)

logger.debug('Parsing configured traps in %s',cmd_args.config)
config_traps = [ s for s in config_p.sections() if s.startswith('trap/') ]

spool_dir = config_p.get('common','spooldir') if config_p.has_section('common') else config_default['spooldir']
logger.debug('Going to use %s as a spool directory for traps', spool_dir)

logger.debug('Reading stdin for trap info from snmptrapd')
trap_received = dict( line.split() for line in sys.stdin if len(line.split()) == 2 )

logger.info('Processing snmptrapd received trap')
if not 'SNMPv2-MIB::snmpTrapOID.0' in trap_received:
    logger.error('There is no snmpTrapOID received. Seams stdin does not contains valid SNPMv2 trap, skipping.')
    logger.debug('Stdin content: %s', trap_received)
    sys.exit(0)
else:
    trap_oid = trap_received['SNMPv2-MIB::snmpTrapOID.0']
    trap_processed = 0
    for trap in config_traps:
        logger.debug('Matching trap against %s',config_p.get(trap,'trapOID'))
        if trap_oid == config_p.get(trap,'trapOID').strip('\'"'):
            logger.info('Processing received trap (snmpTrapOID = %s) according do configuration in [%s] section.', trap_oid, trap)
            trap_processed = 1
            trap_key = config_p.get(trap,'trapKey').strip('\'"')
            if trap_key in trap_received:
                trap_value = config_p.get(trap,'trapValue').strip('\'"')
                if trap_value == trap_received[trap_key]:
                    logger.info('Received trap value (%s) matched configured criteria. Passing trap to handler.', trap_value)
                    try:
                        open(spool_dir + '/' + trap.lstrip('trap/'), 'a').close()
                    except IOError:
                        logger.critical('Failed to create trap file in spool dir: %s', spool_dir)
                        sys.exit(1)
                else:
                    logger.info('Value in trap (%s) is not equal to configured treshold (%s), skiping trap handling.', trap_received[trap_key], trap_value)
            else:
                loggger.info('There is no key %s in the trap received, skipping trap handling.', trap_key)
if not trap_processed: 
    logger.info('Processing of received trap (snmpTrapOID = %s) is not configured. Skipping.', trap_oid)
    logger.debug('Unprocessed trap content: %s', trap_received)

