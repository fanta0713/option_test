import re
from api.os import BaseApi
from utils.ssh_utils import SSHClient
from utils.logging_config import logger

class MetaX(BaseApi):
    def __init__(self, vendor_info, vendor_id, ssh_info):
        self.vendor = vendor_info
        self.vendor_id = vendor_id
        self.ssh_client = SSHClient(ssh_info)
    
    def api_get_gpu_bus_ids(self) -> list:
        command = f"lspci | grep -i {self.vendor_id}"
        result = self.ssh_client.execute_command(command)
        busid_pattern = r'([a-fA-F0-9]{2}[:][0-9]{2}[.]0)'
        busids = re.findall(busid_pattern, result)
        return busids
    
    def api_get_gpu_slot(self, gpu_bus_id) -> str:
        command = f"lspci -vvvs {gpu_bus_id}"
        result = self.ssh_client.execute_command(command)
        slot_pattern = r"\s+Physical\s+Slot:\s+(\d+)"
        slot_id = re.search(slot_pattern, result)
        return slot_id.group(1)
    
    def api_run_pcie_benchmark():
        pass

    def api_run_p2p_benchmark():
        pass

    def api_run_gemm_benchmark():
        pass
