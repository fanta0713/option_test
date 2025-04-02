from abc import ABC, abstractmethod
from utils.ssh_utils import SSHClient

class BaseApi(ABC):

    @abstractmethod
    def get_gpu_bus_ids():
        pass
    @abstractmethod
    def run_pcie_benchmark():
        pass

    @abstractmethod
    def run_p2p_benchmark():
        pass

    @abstractmethod
    def run_gemm_benchmark():
        pass

