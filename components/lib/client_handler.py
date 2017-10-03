import os
import psutil


class ClientHandler:
    """ClientHadler class to get client's information."""

    def __init__(self):
        pass

    def send_client_stats(self):
        """send_client_stats method to fetch client memory/cpu usage."""
        try:
            client_stats = {}
            client_stats['cpu'] = psutil.cpu_percent()
            client_stats['memory'] = psutil.virtual_memory().percent
            return client_stats
        except Exception as error:
            print(error.message)
            return None

    def send_process_stat(self, pid):
        """send_process_stat method for a process running at client."""
        try:
            process_instance = psutil.Process(pid)
            process_stats = {}
            process_stats['memory'] = process_instance.memory_percent()
            process_stats['cpu'] = process_instance.cpu_percent()
            return process_stats
        except Exception as error:
            print(error.message)
            return None

    def reboot_client(self):
        """reboot_client method to reboot remote client."""
        try:
            os.system('reboot')
        except Exception as error:
            print(error.message)

    def send_camera_shot(self):
        """send_camera_shot method to get a snap from client side camera."""
        # code goes here

    def send_client_details(self):
        """send_client_details method to get details of cliet machine."""
        # code goes here
