
import logging
import subprocess

# Enable logging
def get_logger(logger_name, log_format=None, level=logging.INFO):
    if not log_format:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=log_format, level=level)
    return logging.getLogger(logger_name)

def run_shell_cmd(cmds):
    proc = subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.communicate()
