import logging

'''set the logging level to debug. The default level is Warning, if left to default
it will only log warning, error and critical level discarding the debug and info level
Also specify the log file where the information will be logged. The format specifies
, here, the time of log, name of log level (e.g debug, info, warning, error, critical)
and the message as the content of log.'''

logging.basicConfig(filename = 'articles.log', level = logging.DEBUG, format = '%(asctime)s:%(levelname)s:%(message)s')

def log_debug_message(log_msg):
    '''returns debug level of log message'''
    return logging.debug(log_msg)

def log_info_message(log_msg):
    '''returns info level of log message'''
    return logging.info(log_msg)

def log_warning_message(log_msg):
    '''returns warning level of log message'''
    return logging.warning(log_msg)

def log_error_message(log_msg):
    '''returns error level of log message'''
    return logging.error(log_msg)

def log_critical_message(log_msg):
    '''returns critical level of log message'''
    return logging.critical(log_msg)
