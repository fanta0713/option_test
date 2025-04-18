import pytest
from utils.logging_config import logger


@pytest.mark.T21_P1876
def test_graphics_card(get_graphics_card):
    graphics_card = get_graphics_card
    bus_ids = graphics_card.api_get_gpu_bus_ids()
    gpu_pci_detail = get_graphics_card.api_get_gpu_slot(bus_ids[0])
    logger.info(gpu_pci_detail)