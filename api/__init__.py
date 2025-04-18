from abc import ABC, abstractmethod
from utils.ssh_utils import SSHClient

class BaseApi(ABC):

    @abstractmethod
    def api_get_gpu_bus_ids() -> list:
        pass

    @abstractmethod
    def api_get_gpu_slot() -> str:
        pass

    @abstractmethod
    def api_run_pcie_benchmark():
        pass

    @abstractmethod
    def api_run_p2p_benchmark():
        pass

    @abstractmethod
    def api_run_gemm_benchmark():
        pass

