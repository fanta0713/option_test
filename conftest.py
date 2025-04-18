import pytest
import yaml
import os
from api.gpu_api_metax import MetaX
def load_config():
    root_path = os.getcwd()
    config_path = os.path.join(root_path, 'config')
    with open(f'{config_path}/env_config.yaml', 'r') as f:
        return yaml.safe_load(f)

@pytest.fixture(params=[load_config()['vendor']])
def vendor_info(request):
    return request.param

@pytest.fixture(params=[load_config()['vendor_id']])
def vendor_id(request):
    return request.param

@pytest.fixture(params=[load_config()['ssh']])
def ssh_info(request):
    return request.param

@pytest.fixture
def get_graphics_card(vendor_info, vendor_id, ssh_info):
    if vendor_info == "NVIDIA":
        pass
    elif vendor_info == "AMD":
        pass
    elif vendor_info == "MetaX":
        return MetaX(vendor_info, vendor_id, ssh_info)
    else:
        raise ValueError(f"不支持的厂商: {vendor_info}")