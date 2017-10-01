import os
import psutil

from logger import Logger


logger_params = {'file_name': 'error.log',
                 'file_handler': True,
                 'stream_handler': False}

logger_instance = Logger(**logger_params)


class Machine:
    """Machine class to handle client machine level tasks."""

    def __init__(self):
        pass

    def get_machine_stat(self):
        """get_machine_stat method to return machine resource usage."""
        try:
            machine_stat = {}
            machine_stat[
                'virtual_memory_usage'] = psutil.virtual_memory().percent
            machine_stat['cpu_usage'] = psutil.cpu_percent()
            return machine_stat
        except Exception as error:
            return None
            logger_instance.logger.error(
                'Machine::get_machine_stat:{}'.format(error.message))

    def reboot(self):
        """reboot method to reboot client machine."""
        try:
            os.system('reboot')
        except Exception as error:
            logger_instance.logger.error(
                'Machine::reboot:{}'.format(error.message))
