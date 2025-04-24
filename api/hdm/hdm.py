import json
import jsonpath
from api.hdm.hdm_api import HDMApi

class HDM():
    def __init__(self, root_url, login_url, user_info):
        self.hdm_client = HDMApi(root_url, login_url, user_info)
        self.root_url = root_url

    def get_hdm_gpu_vendor(self, bus_id):
        """
        获取HDM GPU厂商信息
        :param bus_id: GPU的bus id
        :return: GPU厂商信息
        """
        data = self.hdm_client.api_get_pcie_device_list()
        data = json.loads(data)
        pcie_devices = data.get("Members", [])
        for device in pcie_devices:
            if device.get("Links").get("PCIeFunctions")[0].get("Oem").get("Public").get("BDF").lower() == f"0000:{bus_id}":
                vendor = device.get("CardManufacturer")
                return vendor
    
    def get_hdm_gpu_speed(self, bus_id):
        """
        获取HDM GPU的速度
        :param bus_id: GPU的bus id
        :return: GPU的最大速度，协商速度
        """
        data = self.hdm_client.api_get_pcie_device_list()
        data = json.loads(data)
        pcie_devices = data.get("Members", [])
        for device in pcie_devices:
            bdf = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.BDF")
            if bdf and str(bdf[0]).lower() == f"0000:{bus_id}":
                max_speed = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.MaxSpeed")
                negotiated_speed = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.Negotiatedspeed")
                return max_speed[0] if max_speed else None, negotiated_speed[0] if negotiated_speed else None

    def get_hdm_gpu_width(self, bus_id):
        """
        获取HDM GPU的通道宽度
        :param bus_id: GPU的bus id
        :return: GPU的最大宽度，协商宽度
        """
        data = self.hdm_client.api_get_pcie_device_list()
        data = json.loads(data)
        pcie_devices = data.get("Members", [])
        for device in pcie_devices:
            bdf = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.BDF")
            if bdf and str(bdf[0]).lower() == f"0000:{bus_id}":
                max_width = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.MaxDatawidth")
                negotiated_width = jsonpath.jsonpath(device, "$.Links.PCIeFunctions[0].Oem.Public.Datawidth")
                return max_width[0] if max_width else None, negotiated_width[0] if negotiated_width else None