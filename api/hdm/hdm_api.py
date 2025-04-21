from utils.http_utils import ApiClient

class HDMApi():    
    def __init__(self, root_url, login_url, user_info):
        self.hdm_client = ApiClient(root_url, login_url, user_info)
        self.root_url = root_url

    def api_get_pcie_device(self, device_id) -> dict:
        url = f"{self.root_url}/Chassis/1/PCIeDevices/{device_id}"
        return self.hdm_client.get(url)

