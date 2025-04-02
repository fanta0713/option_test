from api import BaseApi
from utils.ssh_utils import SSHClient
from utils.logging_config import logger

class MetaX(BaseApi):
    def __init__(self, vendor_info, ssh_info):
        self.vendor = vendor_info
        self.ssh_client = SSHClient(ssh_info)
    
    def get_gpu_bus_ids(self):
        command = f"lspci | grep -i display"
        result = self.ssh_client.execute_command(command)
        return result

    def run_pcie_benchmark():
        pass

    def run_p2p_benchmark():
        pass

    def run_gemm_benchmark():
        pass
