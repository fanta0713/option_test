import re
from api.os import BaseApi
from utils.ssh_utils import SSHClient
from utils.logging_config import logger

class YingXi(BaseApi):
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
        command = f"lspci -xxxvvvs {gpu_bus_id}"
        result = self.ssh_client.execute_command(command)
        slot_pattern = r"\s+Physical\s+Slot:\s+(\d+)"
        slot_id = re.search(slot_pattern, result)
        return slot_id.group(1)
    
    def api_get_gpu_speed_and_bandwidth(self, gpu_bus_id) -> dict:
        command = f"lspci -xxxvvvs {gpu_bus_id}"
        result = self.ssh_client.execute_command(command)
        pattern = r'LnkSta:\s+Speed (\d+(?:\.\d+)?).*Width x(\d+)\s\((\S+)\)'
        speed_and_bandwidth = re.search(pattern, result)
        if speed_and_bandwidth.group(3) != "ok":
            raise ValueError(f"带宽状态异常，当前状态为{speed_and_bandwidth.group(3)}")
        return {"speed": speed_and_bandwidth.group(1), "bandwidth": speed_and_bandwidth.group(2)}
    
    def api_get_gpu_dmi(self, gpu_bus_ids: list) -> list:
        command = f"dmidecode -t 9"
        response = self.ssh_client.execute_command(command)
        pattern = re.compile(
            r'Handle\s+0x[\dA-F]+.*?'
            r'Designation:\s+Slot\s+(\d+).*?'
            r'Current\s+Usage:\s+([^\n]+).*?'
            r'Bus\s+Address:\s+0000:([\da-fA-F:.]{7})',
            re.DOTALL | re.IGNORECASE
            )

        results = []
        for match in pattern.finditer(response):
            slot = match.group(1)
            status = match.group(2).strip()
            bdf = match.group(3).lower()  # 统一为小写
    
            if bdf in gpu_bus_ids:
                results.append({
                    "bus_id": bdf,
                    "slot": slot,
                    "current_usage": status
                })
        return results
    
    def api_run_pcie_benchmark():
        pass

    def api_run_p2p_benchmark():
        pass

    def api_run_gemm_benchmark():
        pass
